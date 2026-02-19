"""
Custom logger configuration using loguru.
"""
import sys
from pathlib import Path
from loguru import logger


class Logger:
    """Custom logger wrapper around loguru."""
    
    _initialized = False
    
    @classmethod
    def setup(cls):
        """Setup logger configuration."""
        if cls._initialized:
            return
        
        # Remove default logger
        logger.remove()
        
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Console handler with custom format
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
            colorize=True,
        )
        
        # File handler for all logs
        logger.add(
            log_dir / "test_execution.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="10 days",
            compression="zip",
        )
        
        # File handler for errors only
        logger.add(
            log_dir / "errors.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
        )
        
        cls._initialized = True
        logger.info("Logger initialized successfully")
    
    @staticmethod
    def get_logger(name: str = __name__):
        """
        Get logger instance.
        
        Args:
            name: Logger name (typically __name__)
            
        Returns:
            Logger instance
        """
        Logger.setup()
        return logger.bind(name=name)


# Initialize logger on import
Logger.setup()
