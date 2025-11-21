async def otp_format_signin(user_name, otp):
    return {
        'subject_': 'Your OPC account: Access from new web or mobile device',
        'body_': f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; color: #333333;">
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f4f4f4; padding: 40px 0;">
                <tr>
                    <td align="center">
                        
                        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            
                            <tr>
                                <td style="background-color: #000000; padding: 40px 30px; text-align: center;">
                                    
                                    <img src="https://code-hamster-rohit1008.github.io/image_repo/logo.png" 
                                         alt="OPC Logo" 
                                         width="150"
                                         style="display: inline-block; max-width: 100%; height: auto; margin-bottom: 20px;">
                                    <h1 style="color: #FFD700; margin: 0; font-size: 24px; letter-spacing: 1px; text-transform: uppercase;">OPC Security</h1>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 40px 30px;">
                                    <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;">Dear {user_name},</p>
                                    <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6;">
                                        It looks like you are trying to sign-in to your OPC account from a new device. To ensure the security of your account, please use the code below.
                                    </p>

                                    <div style="background-color: #FFF9C4; border: 2px dashed #FFD700; border-radius: 4px; padding: 20px; text-align: center; margin: 30px 0;">
                                        <span style="font-size: 32px; font-weight: bold; color: #000000; letter-spacing: 5px; display: block;">
                                            {otp}
                                        </span>
                                    </div>

                                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #666; line-height: 1.5;">
                                        This email was sent because someone attempted to sign in with your <b>correct email and password</b>.
                                    </p>
                                    
                                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #666; line-height: 1.5;">
                                        If this was not you, please <a href="#" style="color: #d4af37; text-decoration: underline;">reset your password</a> immediately.
                                    </p>
                                    
                                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

                                    <p style="margin: 0; font-size: 16px; font-weight: bold;">Best regards,</p>
                                    <p style="margin: 5px 0 0 0; font-size: 16px;">The OPC Team</p>
                                </td>
                            </tr>

                            <tr>
                                <td style="background-color: #333333; padding: 20px; text-align: center; font-size: 12px; color: #bbbbbb;">
                                    <p style="margin: 0;">&copy; 2025 OPC. All rights reserved.</p>
                                    <p style="margin: 5px 0 0 0;">Please do not reply to this automated message.</p>
                                </td>
                            </tr>
                        </table>

                    </td>
                </tr>
            </table>
        
        </body>
        </html>
        """
    }

async def otp_format_signup(user_name, otp):
    return {
        'subject_': 'Welcome to OPC: Confirm Your Email Address',
        'body_': f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; color: #333333;">
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f4f4f4; padding: 40px 0;">
                <tr>
                    <td align="center">
                        
                        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            
                            <tr>
                                <td style="background-color: #000000; padding: 40px 30px; text-align: center;">
                                    
                                    <img src="https://code-hamster-rohit1008.github.io/image_repo/logo.png" 
                                         alt="OPC Logo" 
                                         width="150"
                                         style="display: inline-block; max-width: 100%; height: auto; margin-bottom: 20px;">
                                    <h1 style="color: #FFD700; margin: 0; font-size: 24px; letter-spacing: 1px; text-transform: uppercase;">Welcome to OPC</h1>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 40px 30px;">
                                    <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;">Hello and welcome, {user_name}!</p>
                                    <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6;">
                                        Thank you for signing up with OPC. To complete your registration, please use the verification code below to confirm your email address.
                                    </p>
                                    <div style="background-color: #FFF9C4; border: 2px dashed #FFD700; border-radius: 4px; padding: 20px; text-align: center; margin: 30px 0;">
                                        <span style="font-size: 32px; font-weight: bold; color: #000000; letter-spacing: 5px; display: block;">
                                            {otp}
                                        </span>
                                    </div>
                                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #666; line-height: 1.5;">
                                        If you did not sign up for an OPC account, please ignore this email.
                                    </p>
                                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                                    <p style="margin: 0; font-size: 16px; font-weight: bold;">Best regards,</p>
                                    <p style="margin: 5px 0 0 0; font-size: 16px;">The OPC Team</p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #333333; padding: 20px; text-align: center; font-size: 12px; color: #bbbbbb;">
                                    <p style="margin: 0;">&copy; 2025 OPC. All rights reserved.</p>
                                    <p style="margin: 5px 0 0 0;">Please do not reply to this automated message.</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    }

async def signup_confirmation_email(user_name):
    return {
        'subject_': 'Welcome to OPC!',
        'body_': f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; color: #333333;">
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f4f4f4; padding: 40px 0;">
                <tr>
                    <td align="center">
                        
                        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            
                            <tr>
                                <td style="background-color: #000000; padding: 40px 30px; text-align: center;">
                                    
                                    <img src="https://code-hamster-rohit1008.github.io/image_repo/logo.png" 
                                         alt="OPC Logo" 
                                         width="150"
                                         style="display: inline-block; max-width: 100%; height: auto; margin-bottom: 20px;">
                                    <h1 style="color: #FFD700; margin: 0; font-size: 24px; letter-spacing: 1px; text-transform: uppercase;">Welcome to OPC</h1>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 40px 30px;">
                                    <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;">Dear {user_name},</p>
                                    <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6;">
                                        Welcome to the OPC community! We're thrilled to have you on board.
                                    </p>

                                    <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;">
                                        At OPC, we're committed to providing you with the best experience possible. If you have any questions or need assistance, our support team is here to help.
                                    </p>
                                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                                    <p style="margin: 0; font-size: 16px; font-weight: bold;">Best regards,</p>
                                    <p style="margin: 5px 0 0 0; font-size: 16px;">The OPC Team</p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #333333; padding: 20px; text-align: center; font-size: 12px; color: #bbbbbb;">
                                    <p style="margin: 0;">&copy; 2025 OPC. All rights reserved.</p>
                                    <p style="margin: 5px 0 0 0;">Please do not reply to this automated message.</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    }

async def password_reset_email(user_name, otp):
    return {
        'subject_': 'OPC Password Reset Request',
        'body_': f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; color: #333333;">
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f4f4f4; padding: 40px 0;">
                <tr>
                    <td align="center">
                        
                        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            
                            <tr>
                                <td style="background-color: #000000; padding: 40px 30px; text-align: center;">
                                    
                                    <img src="https://code-hamster-rohit1008.github.io/image_repo/logo.png" 
                                         alt="OPC Logo" 
                                         width="150"
                                         style="display: inline-block; max-width: 100%; height: auto; margin-bottom: 20px;">
                                    <h1 style="color: #FFD700; margin: 0; font-size: 24px; letter-spacing: 1px; text-transform: uppercase;">OPC Password Reset</h1>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 40px 30px;">
                                    <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;">Hello {user_name},</p>
                                    <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6;">
                                        We received a request to reset your OPC account password. Please use the verification code below to proceed with resetting your password.
                                    </p>
                                    <div style="background-color: #FFF9C4; border: 2px dashed #FFD700; border-radius: 4px; padding: 20px; text-align: center; margin: 30px 0;">
                                        <span style="font-size: 32px; font-weight: bold; color: #000000; letter-spacing: 5px; display: block;">
                                            {otp}
                                        </span>
                                    </div>
                                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #666; line-height: 1.5;">
                                        If you did not request a password reset, please ignore this email. Your password will remain unchanged.</p>
                                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                                    <p style="margin: 0; font-size: 16px; font-weight: bold;">Best regards,</p>
                                    <p style="margin: 5px 0 0 0; font-size: 16px;">The OPC Team</p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #333333; padding: 20px; text-align: center; font-size: 12px; color: #bbbbbb;">
                                    <p style="margin: 0;">&copy; 2025 OPC. All rights reserved.</p>
                                    <p style="margin: 5px 0 0 0;">Please do not reply to this automated message.</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    }

async def register_event_email(event_name):
    return {
        'subject_': 'New Event Registered',
        'body_': f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; color: #333333;">
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f4f4f4; padding: 40px 0;">
                <tr>
                    <td align="center">
                        
                        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            
                            <tr>
                                <td style="background-color: #000000; padding: 40px 30px; text-align: center;">
                                    
                                    <img src="https://code-hamster-rohit1008.github.io/image_repo/logo.png" 
                                         alt="OPC Logo" 
                                         width="150"
                                         style="display: inline-block; max-width: 100%; height: auto; margin-bottom: 20px;">
                                    <h1 style="color: #FFD700; margin: 0; font-size: 24px; letter-spacing: 1px; text-transform: uppercase;">New Event Notification</h1>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 40px 30px;">
                                    <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;">Hello,</p>
                                    <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6;">
                                        A new event titled "<b>{event_name}</b>" has been successfully registered in the OPC system.
                                    </p>
                                    <p style="margin: 0 0 15px 0; font-size: 12px; line-height: 1.2;">
                                        To fully manage and view details of this event, please log in to the OPC Dashboard.
                                    </p>
                                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                                    <p style="margin: 0; font-size: 16px; font-weight: bold;">Best regards,</p>
                                    <p style="margin: 5px 0 0 0; font-size: 16px;">The OPC Team</p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #333333; padding: 20px; text-align: center; font-size: 12px; color: #bbbbbb;">
                                    <p style="margin: 0;">&copy; 2025 OPC. All rights reserved.</p>
                                    <p style="margin: 5px 0 0 0;">Please do not reply to this automated message.</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    }