from hashlib import md5
import yaml
import logging
from logging.handlers import TimedRotatingFileHandler

def check_token(token: str) -> bool:
    """
    The function checks if the token hash is in the list of allowed tokens.
    
    Args:
        token (bytes): Token.
        
    Returns:
        None.
    """
    token_md5 = md5(token.encode('utf-8')).hexdigest()

    with open('secrets.txt', 'r') as file:
        hash = file.readline().strip()
        if hash == token_md5:
            return True
    
    return False

def add_hash(token: bytes) -> None:
    """
    The function adds the token hash to the list of allowed tokens.
    
    Args:
        token (bytes): Token.
        
    Returns:
        None.
    """
    with open('secrets.txt', 'a') as file:
        file.write(md5(token.encode('utf-8')).hexdigest())
        file.write('\n')

def load_settings():
    with open('settings.yaml', 'r') as file:
        settings = yaml.load(file, Loader=yaml.loader.BaseLoader)
        return settings

def getLogger(name: str) -> logging.Logger:
    """
    Returns a logger object with the specified name.
    
    Args:
        name (str): The name of the logger.
        
    Returns:
        logging.Logger: The logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    log_handler = TimedRotatingFileHandler(f"logs/{name}.log", encoding='utf-8', when='D')
    log_formatter = logging.Formatter(u"%(name)s %(asctime)s %(levelname)s %(message)s")
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    return logger
