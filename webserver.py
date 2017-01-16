import SimpleHTTPServer
import SocketServer
import os

PORT = 8000
rootPath = "/Users/nikol/Documents/GitHub/MotionCam/MotionCam/motionCaptureImages/"

os.chdir(rootPath)

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving folder: ", rootPath
print "serving at port", PORT

httpd.serve_forever()
