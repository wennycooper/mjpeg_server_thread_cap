# -*- coding: utf-8 -*-
# Convert RTSP stream to MJPEG stream of http
# Editor: Andrew Chiou & KKUEI

import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import cv2
import re
import sys
print(sys.path)
import socket

if len(sys.argv) < 2 :
    print("usage : python3 mjpeg_server.py <quality> <port>")
    # quality from 0 to 100 (the higher is the better). 
    cameraQuality = 30
    port = 8880
else:
    cameraQuality = sys.argv[1]
    port = int(sys.argv[2])

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #self.Det = detect_main()
        global cameraQuality
        try:
            self.path=re.sub('[^.a-zA-Z0-9]', "",str(self.path))
            if self.path=="" or self.path==None or self.path[:1]==".":    # if not our format, return and exit
                self.send_response(200)
                self.end_headers()
                message =  threading.currentThread().getName()
                self.wfile.write(message.encode())
                return    
            
            if self.path.endswith("kla001.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/47da798e-4a56-bbd4-6dc2-fc145523f83a?stream=1'
            elif self.path.endswith("kla002.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/fd7800bb-cab4-1f08-483f-05e033a2ea5b?stream=1'
            elif self.path.endswith("kla003.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/cf53dae1-4c64-b818-b7f5-7887b28c4a40?stream=1'
            elif self.path.endswith("kla004.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/d61ac1ae-f57e-6075-308d-58b18efbce0b?stream=1'
            elif self.path.endswith("kla005.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/b30f6b90-f0e7-7910-ae8d-b869d5e65b1e?stream=1'
            elif self.path.endswith("klb001.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/4ee71a53-6084-e6d9-243e-8e488fff9234?stream=1'
            elif self.path.endswith("klb002.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/2a1f4af7-da5f-67c6-3dc3-a4c7365fde86?stream=1'
            elif self.path.endswith("klb003.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/c02c701c-8412-b470-3cce-c13d096e10be?stream=1'
            elif self.path.endswith("klc001.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/25f7969d-8ca6-ccdc-c1e7-e7faf0278a32?stream=1'                          
            elif self.path.endswith("khc001.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/1d0e57ae-9e73-04e5-205c-9a7a1c07863e?stream=1'
            elif self.path.endswith("khc002.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/a53117e5-a570-f31f-9fce-d1b3437986a9?stream=1'
            elif self.path.endswith("khc006.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/72c48c0c-f308-40b2-b25f-68ba2b490c32?stream=1'
            elif self.path.endswith("kha004.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/d9e41f6f-8817-5b13-1122-9f421584f636?stream=0'
            elif self.path.endswith("khc007.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/8c1232bb-28de-a5c8-2260-b77aa74e871f?stream=1'
            elif self.path.endswith("khc005.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/09aa6fb1-de6b-60c0-3d3c-f00aa99a7575?stream=1'
            elif self.path.endswith("mst999.mjpeg"):
                self.URL = 'rtsp://demo:demo@III@10.22.101.30:7001/6095fd6a-42bf-9a63-bae1-60272d38161c?stream=1'
            else:
                self.sendresponse(200)
                self.end_headers()
                message = threading.currentThread().getName()
                self.wfile.write(message.encode())
                return    # exit the thread

            capture = cv2.VideoCapture(self.URL)

            self.send_response(200)
            self.send_header("Content-type", "multipart/x-mixed-replace; boundary=--jpegboundary")
            self.end_headers()
            
            while 1:
                ret, img1 = capture.read()

                if ret:
                    try:
                        img1 = cv2.resize(img1, (640, 360), interpolation=cv2.INTER_CUBIC)
                        cv2mat1 = cv2.imencode(".jpeg", img1, [cv2.IMWRITE_JPEG_QUALITY, cameraQuality])[1]
                        self.wfile.write("--jpegboundary\r\n".encode("utf-8"))
                        self.send_header("Content-type", "image/jpeg")
                        self.send_header("Content-length", str(cv2mat1.size))
                        self.end_headers()
                        self.wfile.write(cv2mat1.tobytes())                    
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        print('Connection is closed')
                        break
                time.sleep(0.02) 
            return
        except ConnectionAbortedError:
            print('Connection is closed')
            # exit the thread gracefully
             
        except IOError:
            self.send_error(404,'Target Not Found: %s' % self.path)    
    

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():

    while 1:
        try:
            server = ThreadedHTTPServer(('0.0.0.0', port), MyHandler)
            print('starting MJPEG Server...')
            print('see <local IP>:'+ str(port) + '/kla001.mjpeg (default)')
            server.serve_forever()
        except KeyboardInterrupt:
            print('^C received, shutting down server')
            server.socket.close()
            return

if __name__ == '__main__':
    main()
