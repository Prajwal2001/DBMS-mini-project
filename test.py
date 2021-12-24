import smtplib

sender_mail = "textacct.2001@gmail.com"
receivers_mail = "kulkarniprajwal.01@gmail.com"

msg = """From: From Person %s  
To: To Person %s  
  
MIME-Version:1.0  
Content-type:text/html  
  
  
Subject: Sending SMTP e-mail   
  
<h1> test </h1>
<hr>
<p>This is a test mail</p>
<table>
<tr> 
<td> col1 </td>
<td> col2 </td>
</tr>
<tr>
<td> Prajwal </td>
<td> Kulkarni </td>
</tr>
</table>
""" % (sender_mail, receivers_mail)

connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=sender_mail, password="text@2001")
connection.sendmail(from_addr=sender_mail,
                    to_addrs=receivers_mail, msg=msg)
connection.close()
