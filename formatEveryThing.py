import sublime
import sublime_plugin
import webbrowser
import json
import urllib.parse
import urllib.request
import socket  
import functools
import traceback
import datetime; 

def myformat(source):
    # print("source="+source)
    if source=="":
       return ""
    url = 'http://alioo.online/format/format.json'
    #header
    headers={
        'Content-type':'application/x-www-form-urlencoded',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host':'alioo.online',
        'Origin':'http://alioo.sublime.com',
        'Referer':'http://alioo.sublime.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'
    }

    data={
        "source":source
    }
    #encode
    data=urllib.parse.urlencode(data).encode('utf-8')
    
    # timeout in seconds 
    timeout = 2
    socket.setdefaulttimeout(timeout)  

    req =  urllib.request.Request(url, headers=headers, data=data)
    page = urllib.request.urlopen(req).read()
    page = page.decode('utf-8')
    # print("page="+page)
    pagejson = json.loads(page)
    target=pagejson['target']
    # print("type(target)","=", type(target) )

    return target;


class FormatEveryThingCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        # sz=self.view.size()
        # region=sublime.Region(0,sz)
        # source=self.view.substr(region)
        # self.view.insert(edit, self.view.size(), "\n#Formating start,please wait\n")
        # print("Formating start,please wait")
        # myformat(source,self,edit,region)
        # sublime.set_timeout_async(self.process, 0)
        # sublime.set_timeout_async(functools.partial(self.process,edit, "hahhaha") , 0)
        # slef.view.run_command("format", {"line": line})
        allRegion=sublime.Region(0, self.view.size());
        source = self.view.substr(allRegion)

        sublime.status_message('startting')
        self.view.run_command("format", {"source": source})
        
    # time consuming task placed in a asycn thread
    # def process(self,edit,str):
    #     # print("str="+str)
    #     # print("type(self.view)","=",type(self.view))
    #     # print("type(edit)","=",type(edit))
    #     # sublime.status_message('FormatEveryThing startting')
    #     # # get the content
    #     # allRegion=sublime.Region(0, self.view.size());
    #     # source = self.view.substr(allRegion)
    #     # self.view.insert(edit, 0, "lllllllllzzzzzzzz")
    #     # target = myformat(self,edit,source)
    #     # print("target="+target);
    #     try:
    #         # allRegion=sublime.Region(0, self.view.size())
    #         # source = self.view.substr(allRegion)
    #         print("self.view.size()=",self.view.size())
    #         # self.view.end_edit(edit)
    #         self.view.insert(edit, 14, "cccccccccccc")
    #     except:
    #         # e = sys.exc_info()[1]
    #         # print(e)
    #         traceback.print_exc()
    #         sublime.error_message('error:\n%s',"lzc is error")
    #     sublime.status_message('FormatEveryThing is end'+str)

class FormatCommand(sublime_plugin.TextCommand):
    def run(self, edit, source):
        sublime.status_message('FormatEveryThing startting')

        starttime = datetime.datetime.now()
        target = myformat(source)
        endtime = datetime.datetime.now()
        usetime=(endtime-starttime).total_seconds()
        # print("target="+target);

        self.view.replace(edit, sublime.Region(0, self.view.size()), "")  #clean screen
        self.view.insert(edit, 0, target )  #output in screen
        sublime.status_message('FormatEveryThing is end,usetime='+str(usetime))
