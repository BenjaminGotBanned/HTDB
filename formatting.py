import json

import requests

class BuiltFunc:
    
    """Class used to represent all the built in features of HTDB"""
    
    def process(text):
        
        """Returns the formatted version of a string with functions in it"""
        
        http_requests = text.split("<HTTPRequest")
        
        for request in http_requests:
            
            if request.startswith(" url=\""):
                
                request_url = request.split(" url=\"")[1].split("\"")[0]
                    
                scope = request.split(f"scope=\"")[1].split("\"")[0]
                
                headers = request.split(f"headers=\"")[1].split("\">")[0]
                
                request_data = json.loads(requests.get(request_url, headers = json.loads(headers)).text)[scope]
                
                text = text.replace(f"<HTTPRequest url=\"{request_url}\" scope=\"{scope}\" headers=\"{headers}\">", request_data, 1)
                
        return text
    
class Formatting:
    
    """Represents formatted versions of text"""
    
    def format(text, bot, message = None):
        
            """Returns the formatted version of a string"""
        
            args = ["", "", "", ""]
        
            if message:
            
                margs = message.content.split(" ")[1:]
                
                c = 0
                
                while c < len(margs):
                    
                    args[c] = margs[c]
                    
                    c += 1
                    
                print(args)
        
            formatted_text = text
            
            if message:
                
                formatted_text = text.replace("<user.name>", str(message.author.name))
            
                formatted_text = formatted_text.replace("<user.id>", str(message.author.id))
                
                formatted_text = formatted_text.replace("<user>", str(message.author))
                
                formatted_text = formatted_text.replace("<user.avatar_url>", str(message.author.avatar_url))
            
                formatted_text = formatted_text.replace("<channel.name>", str(message.channel.name))
            
                formatted_text = formatted_text.replace("<channel.id>", str(message.channel.id))
                
                formatted_text = formatted_text.replace("<guild.name>", str(message.guild.name))
                
                formatted_text = formatted_text.replace("<guild.id>", str(message.guild.id))
            
            formatted_text = formatted_text.replace("<bot.name>", str(bot.user.name))
            
            formatted_text = formatted_text.replace("<bot.id>", str(bot.user.id))
            
            formatted_text = formatted_text.replace("<bot.avatar_url>", str(bot.user.avatar_url))
            
            formatted_text = formatted_text.replace("<bot>", str(f"{bot.user.name}#{bot.user.discriminator}"))
            
            formatted_text = formatted_text.replace("<arg1>", str(args[0]))
            
            formatted_text = formatted_text.replace("<arg2>", str(args[1]))
            
            formatted_text = formatted_text.replace("<arg3>", str(args[2]))
            
            formatted_text = formatted_text.replace("<arg4>", str(args[3]))
            
            formatted_text = formatted_text.replace("\\n", "\n")
            
            formatted_text = BuiltFunc.process(formatted_text)
            
            return formatted_text