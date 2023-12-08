import pandas as pd
import winsound
import subprocess
import smtplib,ssl

import pyautogui

pyautogui.click()


file="screen.xlsx"
file2="przekodownik.xlsx"
df=pd.read_excel(file)
przekodownik=pd.read_excel(file2)

print(przekodownik)

row1=[]                     # Lista produktów do arbitraż Base M vs Base Q
for x in przekodownik.iloc[0]:
    row1.append(x)
row2=[]                     # Lista produktów do arbitraż Peak M vs Peak Q
for x in przekodownik.iloc[1]:
    row2.append(x)

print(f'Row 1:{row1}')
print(f'Row 2:{row2}')

df2=df[df['Instrument'].isin(row1)]
df3=df[df['Instrument'].isin(row2)]

# #Funkcja do wysyłania maila z alertem
# def send_mail(message):
#     host = "smtp.gmail.com"
#     port = 465
#     username = "paweltestowy7@gmail.com"
#     password = "wobk saep jtwo bwqy"
#     receiver = "paweltestowy7@gmail.com"
#     context = ssl.create_default_context()
#
#     message="""\
#     From:<paweltestowy7@gmail.com>
#     To: <paweltestowy7@gmail.com>
#     Subject: testowy e-mail
#
#     testowa treść
#     """
#     with smtplib.SMTP_SSL(host,port,context=context) as server:
#         server.login(username,password)
#         server.sendmail(username,receiver,message)


#Funcja sprawdzjąca czy jest możliwość następującego arbitrażu: Sprzedaż miesięcy vs zakup kwartału
def Arb_BID(row):
    df_temp=df[df['Instrument'].isin(row)]
    Arb_BID=df_temp['Bid'].iloc[:3].sum()/3-df_temp['Ask'].iloc[3]
    if Arb_BID>1:
        print('--------------------------------')
        print(f"!!![{df_temp['Instrument'].iloc[0][:4]}]: Arbitraż Sprzedaż miesięcy i zakup kwartału MOŻLIWY !!!\n")
        print(f"Sprzedaż instrumentu  {df_temp['Instrument'].iloc[0]} po kursie BID : {df_temp['Bid'].iloc[0]}")
        print(f"Sprzedaż instrumentu  {df_temp['Instrument'].iloc[1]} po kursie BID : {df_temp['Bid'].iloc[1]}")
        print(f"Sprzedaż instrumentu  {df_temp['Instrument'].iloc[2]} po kursie BID : {df_temp['Bid'].iloc[2]}")
        print(f"Zakup instrumentu     {df_temp['Instrument'].iloc[3]} po kursie ASK: {df_temp['Ask'].iloc[3]}")
        print(f"Spread przy arbitrazu ok.: {int(df_temp['Bid'].iloc[:3].sum()/3-df_temp['Ask'].iloc[3])} PLN")
        print('------------------------------')
        #winsound.PlaySound("x.wav", winsound.SND_FILENAME)
        mail_message=f"""
        !!![{df_temp['Instrument'].iloc[0][:4]}]: Arbitraż Sprzedaż miesięcy i zakup kwartału MOŻLIWY !!!\n
        Sprzedaż instrumentu  {df_temp['Instrument'].iloc[0]} po kursie BID : {df_temp['Bid'].iloc[0]}
        Sprzedaż instrumentu  {df_temp['Instrument'].iloc[1]} po kursie BID : {df_temp['Bid'].iloc[1]}
        Sprzedaż instrumentu  {df_temp['Instrument'].iloc[2]} po kursie BID : {df_temp['Bid'].iloc[2]}
        Zakup instrumentu     {df_temp['Instrument'].iloc[3]} po kursie ASK: {df_temp['Ask'].iloc[3]}
        Spread przy arbitrazu ok.: {int(df_temp['Bid'].iloc[:3].sum()/3-df_temp['Ask'].iloc[3])} PLN
        """
        # send_mail(mail_message)
    elif Arb_BID<1:
        print(f"!!![{df_temp['Instrument'].iloc[0][:4]}]: Arbitraż Sprzedaż miesięcy i zakup kwartału niemożliwy")
    else:
        print('Nie ma wystarczająco danych dla arbitrażu')
    return df_temp

#Funcja sprawdzjąca czy jest możliwość następującego arbitrażu: zakup miesięcy vs sprzedaż kwartału
def Arb_ASK(row):
    df_temp=df[df['Instrument'].isin(row)]
    Arb_ASK=df_temp['Ask'].iloc[:3].sum()/3-df_temp['Bid'].iloc[3]
    if Arb_ASK<-1:
        print('--------------------------------')
        print(f"!!![{df_temp['Instrument'].iloc[0][:4]}]: Arbitraż Zakup miesięcy i sprzedaż kwartału MOŻLIWY !!!\n")
        print(f"Zakup instrumentu  {df_temp['Instrument'].iloc[0]} po kursie ASK : {df_temp['Ask'].iloc[0]}")
        print(f"Zakup instrumentu  {df_temp['Instrument'].iloc[1]} po kursie ASK : {df_temp['Ask'].iloc[1]}")
        print(f"Zakup instrumentu  {df_temp['Instrument'].iloc[2]} po kursie ASK : {df_temp['Ask'].iloc[2]}")
        print(f"Zakup instrumentu  {df_temp['Instrument'].iloc[3]} po kursie BID:  {df_temp['Bid'].iloc[3]}")
        print(f"Spread przy arbitrazu ok.: {-int(df_temp['Ask'].iloc[:3].sum()/3-df_temp['Bid'].iloc[3])} PLN")
        print('------------------------------')
        #winsound.PlaySound("x.wav", winsound.SND_FILENAME)
        winsound.Beep(250,1000)
    elif Arb_ASK>-1:
        print(f"!!![{df_temp['Instrument'].iloc[0][:4]}]:Arbitraż zakup miesięcy i sprzedaż kwartału niemożliwy")
    else:
        print('Nie ma wystarczająco danych dla arbitrażu')
    return df_temp


Arb_BID(row1)
Arb_BID(row2)
Arb_ASK(row1)
Arb_ASK(row2)


