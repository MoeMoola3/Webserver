from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

tasklist = {}
nameFound ={}

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/tasklist'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Contacts</h1>'
            output += '<h3><a href="/tasklist/new">Add a new contact</a><h3/>'
            for task, taskvalue in tasklist.items():
                output += task[2:-2]
                output += ' - '
                output += taskvalue[2:-2]
                output += '<a/ href="/tasklist/%s/remove"> X</a>' % task
                output += '</br>'
            output += '<a/href="/tasklist/%s/search">Search</a>'
            output += '<body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Add a new contact</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/new">'
            output += '<input name="name" type="text" placeholder="Name">'
            output += '<input name="number" type="text" placeholder="Number">'
            output += '<input type="submit" value="Add">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            print(listIDPath)
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Remove : %s</h1>' % listIDPath.replace('%20', ' ')[2:-2]
            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/%s/remove">' % listIDPath
            output += '<input type="submit" value="Remove"></form>'
            output += '<a href="/tasklist">Cancel</a>'
            output += '</body></html>'            

            self.wfile.write(output.encode())

        if self.path.endswith('/search'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Search for contact</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/search">'
            output += '<input name="searchName" type="text" placeholder="Name">'
            output += '<input type="submit" value="Search">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

        if self.path.endswith('/contact'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Contact Number</h1>'
            print("this issss "+ nameFound["fdName"])
            print("this isss"+ tasklist[nameFound["fdName"]])
            output += tasklist[nameFound["fdName"]][2:-2]
            # output += nameFound["fdName"]
            # print("this is "+ nameFound)

            output += '</body></html>' 

            self.wfile.write(output.encode())    


    
    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype =='multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                # new_task = fields.get('task')
                # tasklist.append(new_task[0])
                new_name = fields.get('name')
                new_num = fields.get('number')
                print(new_name + new_num)
                # tasklist(new_name).append(new_num)
                new_name_s =str(new_name)
                new_num_s = str(new_num)

                tasklist[new_name_s]=new_num_s
                # for x in tasklist.keys():
                #     print(x)

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()

        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            # ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            if ctype == 'multipart/form-data':
                list_item = listIDPath.replace('%20',' ')
                # tasklist.remove(list_item)
                # tasklist.pop(list_item)
                for x in tasklist.keys():
                    print(x)
                del tasklist[list_item]
                print("it reaches here")

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()    

        if self.path.endswith('/search'):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype =='multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)

                sName = fields.get('searchName')
                sName_s = str(sName)
                # nameFound = tasklist.get(sName_s)
                nameFound["fdName"]=sName_s
                # print(tasklist.get(sName_s))
                # print("this is"+nameFound)

                # new_name_s =str(new_name)
                # new_num_s = str(new_num)

                # tasklist[new_name_s]=new_num_s
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/contact')
                self.end_headers() 


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()  