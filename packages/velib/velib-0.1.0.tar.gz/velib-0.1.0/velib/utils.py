#

def password_check(passwd, ch_min=None, ch_max=None, special_symbol=None):
    errors = []
    ch_min = ch_min if ch_min else 6
    ch_max = ch_max if ch_max else 32
    
    if len(passwd) < ch_min:
        errors.append('length should be at least {min}'.format(min=ch_min))
    
    if len(passwd) > ch_max:
        errors.append('length should not be greater than {max}'.format(max=ch_max))
    
    if not any(char.isdigit() for char in passwd):
        errors.append('should have at least one numeral')
    
    if not any(char.isupper() for char in passwd):
        errors.append('should have at least one uppercase letter')
    
    if not any(char.islower() for char in passwd):
        errors.append('should have at least one lowercase letter')
    
    if special_symbol and not any(char in special_symbol for char in passwd):
        errors.append('should have at least one of the symbols {cs}'.format(cs=''.join(special_symbol)))

    if len(errors) > 0:
        return errors
