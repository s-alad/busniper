import smtplib

from email.message import EmailMessage

class Email:
    def __init__(self):
        msg = EmailMessage()
        s = smtplib.SMTP('localhost')

    def send(self, course: str, link: str, email: str):
        self.msg.set_content("""\
        {course} has an EMPTY seat!
        Act quick! Click here[1] to register

        [1] {link}

        """.format(course=course, link=link), subtype='plain')

        self.msg.add_alternative("""\
            <html>
                <body>
                    <h1>{course} has an EMPTY seat!</h1>
                    <p> 
                        Act quick! Click <a href="{link}">here</a> to register 
                    </p>
                </body>
            </html> 
        """.format(course="", link=""), subtype='html')

        self.msg['Subject'] = "{course} has an EMPTY seat!}".format(course="")
        self.msg['From'] = "alert@emptyclass.info"
        self.msg['To'] = "{email}".format(email="")

        self.s.send_message(self.msg)
        self.s.quit()

