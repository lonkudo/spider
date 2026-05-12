import pyotp

def get_totp_from_input(input_string):
    # Step 1: Remove spaces
    clean_secret = input_string.replace(" ", "")

    # Step 2: Generate a TOTP object
    totp = pyotp.TOTP(clean_secret)

    # Step 3: Generate the current TOTP code
    current_totp = totp.now()

    return current_totp
