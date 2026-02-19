"""
Email notification utility for sending test reports.
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
from typing import List
from jinja2 import Template
from utils.logger import Logger
from config.config import Config
import zipfile

logger = Logger.get_logger(__name__)


class EmailNotification:
    """Handle email notifications for test reports."""
    
    def __init__(self):
        """Initialize email notification."""
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.sender_email = Config.SENDER_EMAIL
        self.sender_password = Config.SENDER_PASSWORD
        self.receiver_emails = [email.strip() for email in Config.RECEIVER_EMAILS if email.strip()]
    
    def send_test_failure_notification(
        self,
        test_name: str,
        error_message: str,
        screenshot_path: str = None
    ) -> bool:
        """
        Send immediate notification when a test fails.
        
        Args:
            test_name: Name of failed test
            error_message: Error message
            screenshot_path: Path to screenshot
            
        Returns:
            True if email sent successfully
        """
        if not Config.SEND_EMAIL_ON_FAILURE:
            logger.info("Email on failure is disabled")
            return False
        
        subject = f"❌ Test Failed: {test_name}"
        
        html_body = self._generate_failure_email_body(test_name, error_message)
        
        attachments = []
        if screenshot_path and os.path.exists(screenshot_path):
            attachments.append(screenshot_path)
        
        return self._send_email(subject, html_body, attachments)
    
    def send_test_report(
        self,
        total_tests: int,
        passed: int,
        failed: int,
        skipped: int,
        duration: float,
        include_allure_report: bool = True
    ) -> bool:
        """
        Send complete test execution report.
        
        Args:
            total_tests: Total number of tests
            passed: Number of passed tests
            failed: Number of failed tests
            skipped: Number of skipped tests
            duration: Test execution duration
            include_allure_report: Include Allure report as zip
            
        Returns:
            True if email sent successfully
        """
        if not Config.SEND_EMAIL_REPORT:
            logger.info("Email report is disabled")
            return False
        
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        if failed > 0:
            status = "❌ FAILED"
            emoji = "❌"
        elif total_tests == passed:
            status = "✅ PASSED"
            emoji = "✅"
        else:
            status = "⚠️ PARTIAL"
            emoji = "⚠️"
        
        subject = f"{emoji} Test Report - {status} ({pass_rate:.1f}% Pass Rate)"
        
        html_body = self._generate_report_email_body(
            total_tests, passed, failed, skipped, duration, pass_rate
        )
        
        attachments = []
        
        # Create and attach zip with all reports
        if include_allure_report:
            zip_path = self._create_reports_zip()
            if zip_path:
                attachments.append(zip_path)
        
        return self._send_email(subject, html_body, attachments)
    
    def _send_email(
        self,
        subject: str,
        html_body: str,
        attachments: List[str] = None
    ) -> bool:
        """
        Send email with attachments.
        
        Args:
            subject: Email subject
            html_body: HTML email body
            attachments: List of file paths to attach
            
        Returns:
            True if sent successfully
        """
        if not self.sender_email or not self.sender_password:
            logger.error("Email credentials not configured")
            return False
        
        if not self.receiver_emails:
            logger.error("No receiver emails configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(self.receiver_emails)
            msg['Subject'] = subject
            
            # Attach HTML body
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        self._attach_file(msg, file_path)
            
            # Send email
            logger.info(f"Sending email to: {self.receiver_emails}")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info("✓ Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str) -> None:
        """
        Attach file to email.
        
        Args:
            msg: Email message object
            file_path: Path to file
        """
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        msg.attach(part)
        
        logger.info(f"Attached file: {filename}")
    
    def _generate_failure_email_body(self, test_name: str, error_message: str) -> str:
        """
        Generate HTML email body for test failure.
        
        Args:
            test_name: Test name
            error_message: Error message
            
        Returns:
            HTML string
        """
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #dc3545; color: white; padding: 20px; text-align: center; }
                .content { background: #f8f9fa; padding: 20px; margin-top: 20px; }
                .error { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; }
                .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ Test Failed</h1>
                </div>
                <div class="content">
                    <h2>Test Details</h2>
                    <p><strong>Test Name:</strong> {{ test_name }}</p>
                    <p><strong>Time:</strong> {{ timestamp }}</p>
                    
                    <div class="error">
                        <h3>Error Message:</h3>
                        <pre>{{ error_message }}</pre>
                    </div>
                    
                    <p>Please check the attached screenshot for more details.</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from the Test Automation Framework</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template_obj = Template(template)
        return template_obj.render(
            test_name=test_name,
            error_message=error_message,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _generate_report_email_body(
        self,
        total: int,
        passed: int,
        failed: int,
        skipped: int,
        duration: float,
        pass_rate: float
    ) -> str:
        """
        Generate HTML email body for test report.
        
        Args:
            total: Total tests
            passed: Passed tests
            failed: Failed tests
            skipped: Skipped tests
            duration: Duration in seconds
            pass_rate: Pass rate percentage
            
        Returns:
            HTML string
        """
        status_color = "#28a745" if failed == 0 else "#dc3545"
        
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 700px; margin: 0 auto; padding: 20px; }
                .header { background: {{ status_color }}; color: white; padding: 20px; text-align: center; }
                .summary { display: flex; justify-content: space-around; margin: 20px 0; }
                .stat { text-align: center; padding: 15px; background: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px; }
                .stat-value { font-size: 32px; font-weight: bold; }
                .passed { color: #28a745; }
                .failed { color: #dc3545; }
                .skipped { color: #ffc107; }
                .progress { background: #e9ecef; height: 30px; border-radius: 15px; overflow: hidden; margin: 20px 0; }
                .progress-bar { height: 100%; background: #28a745; text-align: center; line-height: 30px; color: white; }
                .details { background: #f8f9fa; padding: 20px; margin-top: 20px; }
                .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{{ status_emoji }} Test Execution Report</h1>
                    <p>{{ timestamp }}</p>
                </div>
                
                <div class="summary">
                    <div class="stat">
                        <div class="stat-value">{{ total }}</div>
                        <div>Total Tests</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value passed">{{ passed }}</div>
                        <div>Passed</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value failed">{{ failed }}</div>
                        <div>Failed</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value skipped">{{ skipped }}</div>
                        <div>Skipped</div>
                    </div>
                </div>
                
                <div class="progress">
                    <div class="progress-bar" style="width: {{ pass_rate }}%">
                        {{ "%.1f"|format(pass_rate) }}% Pass Rate
                    </div>
                </div>
                
                <div class="details">
                    <h3>Execution Details</h3>
                    <p><strong>Duration:</strong> {{ duration }} seconds</p>
                    <p><strong>Environment:</strong> {{ env }}</p>
                    <p><strong>Browser:</strong> {{ browser }}</p>
                    
                    <h3>📎 Attachments</h3>
                    <p>Complete test reports are attached as a ZIP file including:</p>
                    <ul>
                        <li>Allure Report</li>
                        <li>Screenshots</li>
                        <li>Logs</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from the Test Automation Framework</p>
                    <p>For detailed reports, extract and open the attached ZIP file</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template_obj = Template(template)
        return template_obj.render(
            total=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=round(duration, 2),
            pass_rate=pass_rate,
            status_color=status_color,
            status_emoji="✅" if failed == 0 else "❌",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            env=Config.ENV,
            browser=Config.BROWSER
        )
    
    def _create_reports_zip(self) -> str:
        """
        Create ZIP file with all reports.
        
        Returns:
            Path to ZIP file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_path = f"reports/test_report_{timestamp}.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add allure results
                if os.path.exists("reports/allure-results"):
                    for root, dirs, files in os.walk("reports/allure-results"):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, "reports")
                            zipf.write(file_path, arcname)
                
                # Add screenshots
                if os.path.exists("reports/screenshots"):
                    for root, dirs, files in os.walk("reports/screenshots"):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, "reports")
                            zipf.write(file_path, arcname)
                
                # Add logs
                if os.path.exists("logs"):
                    for root, dirs, files in os.walk("logs"):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, f"logs/{file}")
            
            logger.info(f"Created reports ZIP: {zip_path}")
            return zip_path
            
        except Exception as e:
            logger.error(f"Failed to create reports ZIP: {e}")
            return None
