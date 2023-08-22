import smtplib, ssl
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notification():
    def __init__(self, senderAddress, targetAddress):
        # Obtain email information
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = time.strftime("ScalpNotifier: New items found!")
        self.message["From"] = senderAddress
        self.message["To"] = targetAddress

        self.emailPass = "qphyvapnzduziexh" # Import
        self.senderAddress = senderAddress
        self.targetAddress = targetAddress

    def send(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.senderAddress, self.emailPass)
            server.sendmail(
                self.senderAddress, self.targetAddress, self.message.as_string()
            )

    def email(self, items):
        # Construct message
        content = "Item(s) Located:"

        for i in items:
            content += "\n\t\t• %s" % (', '.join(i[:len(i)]))

        self.message.attach(MIMEText(content, "plain")) # Add html compatibility # TODO
        self.send()

    def betterEmail(self, items):
        innerContent = ""

        for i in range(len(items)):
            # Insert item into bootstrap format
            innerContent += f"""
            <div class="col-xl-3 col-lg-4 col-md-6 mb-4">
                <div class="bg-white rounded shadow-sm">
                    <a href="{items[i][3]}">
                        <img src="{items[i][4]}" alt="" class="img-fluid card-img-top">
                    </a>
                    <div class="p-4">
                        <h5 class="text-muted"><b>{items[i][1]}</b></h5>
                        <p class="small text-muted mb-0"><b>Location: </b>{items[i][2]}</p>
                        <p class="small text-muted mb-0"><b>Price: </b>{items[i][0]}</p>
                    </div>
                </div>
            </div>
            """

        # add inner content and timestamp to base html
        htmlContent = """
            <html>
                <head>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                    <link rel="stylesheet" media="screen" href="https://fontlibrary.org/face/gidole-regular" type="text/css">
                </head>
                <style type="text/css">
                    body {
                        background: #f4f4f4;
                    }
                
                    .banner {
                        background: #a770ef;
                        background: -webkit-linear-gradient(to right, #cc5500, #99431f, #662d15);
                        background: linear-gradient(to right, #cc5500, #99431f, #662d15);
                    }
                </style>
                <body>
                    <div class="container-fluid">
                        <div class="px-lg-5">
                            <div class="row py-5">
                                <div class="col-lg-12 mx-auto">
                                    <div class="text-white p-5 shadow-sm rounded banner">
                                        <h1 class="display-4">ScalpNotifier</h1>
                                        <p class="lead">
                                            %s
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                %s
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        """ % (time.strftime("%A, %B %d at %-I:%M%p"), innerContent)

        self.message.attach(MIMEText(htmlContent, "html"))  # Add html compatibility
        self.send()

