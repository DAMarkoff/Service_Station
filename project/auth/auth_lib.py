
    """The password must be at least 8 chars long and not exceed 32 chars;
    must contain at least one digit, one upper, one lower letter, one special char ['$', '@', '#', '!', '%']
    
    Minimum eight characters, at least one letter and one number:
    "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    
    Minimum eight characters, at least one letter, one number and one special character:
    "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    
    Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
    
    Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    
    
    Minimum eight and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character:
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$"
    
    """


def validate_phone(phone: str) -> bool:
    rx = re.compile(r"\d{10,15}$")
    return True if rx.match(phone) else False
    # return re.fullmatch("\d{10,15}$", phone)
    