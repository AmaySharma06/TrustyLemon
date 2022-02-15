import json
import discord
import time

class Db:
    
    path = "config.json"

    empty_warn_field  = {
        "count" : 0,
        "timestamps" : [],
        "warnings" : []
    }

    """
    warns : {
	"id" : {
		"count" : num
		"timestamps" : [1,2,3]
		"warnings" : [4,5,6]
	    }
    }
    """

    @classmethod
    def get_value(cls,key=None): 
        try:
            with open(cls.path,"r") as file:
                data = json.load(file)
        except KeyError:
            data = {}

        if not key:
            return data

        return data[key]
    
    @classmethod
    def set_value(cls,key,value):
        dic  = cls.get_value()   
        dic[key] = value
        with open(cls.path,"w") as file:
            json.dump(dic,file,indent=4)
    
    @classmethod
    def warn_(cls,member,reason):
        print(member)
        warns = cls.get_value("warns")
        try:
            field = warns[str(member.id)]
        except KeyError:                                       
            field = cls.empty_warn_field
        field["count"] += 1
        field["warnings"].append(reason)
        field["timestamps"].append(time.time())
        warns[str(member.id)] = field
        cls.set_value("warns", warns)


# def check_member(ctx,member):
#     if isinstance(member, discord.Member):
#         return member
#     elif isinstance(member, int):
#         return ctx.guild.get_member(member)
    
