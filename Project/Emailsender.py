import smtplib
try:
    server = smtplib.SMTP("smtp.gmail.com",port=587)
    server.starttls()

    #receiver email
    receiver_mail =input("enterr the receiver mail:")

    #email credential
    sender_mail ="paruljainn916@gmail.com"
    password ="kned invn bpff gfsc"

    #login
    server.login(sender_mail,password)

    #sending email
    subject =("enter the subject:")
    body =input("enter the body:")
    message = f"subject: {subject} \n\n{body}"
    server.sendmail(sender_mail,receiver_mail,message)
    print("mail sent successfullly")
    server.quit()
except Exception as e:
    print("An error occured",e) 
    #mute
