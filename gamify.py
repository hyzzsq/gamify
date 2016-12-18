def initialize():
    '''Initializes the global variables needed for the simulation. 
    '''
    global cur_hedons, cur_health

    global cur_time
    global last_activity, last_activity_duration
    
    global last_finished
    global bored_with_stars
    
    global tired 
    global star_activity,star_num
    global star_list
     
    tired = False
    cur_hedons = 0
    cur_health = 0
    
    star_activity= None
    star_num = 0
    star_list = [] 
    
    cur_star = None
    cur_star_activity = None
    
    bored_with_stars = False
    
    last_activity = None
    last_activity_duration = 0
    
    cur_time = 0
    
    last_finished = -1000
    

            

def star_can_be_taken(activity):
    if activity == star_activity and (not bored_with_stars):
        return True
    return False

    
def perform_activity(activity, duration):
    global cur_hedons, cur_health

    global cur_time
    global last_activity, last_activity_duration
    
    global last_finished
    global bored_with_stars
    
    global tired 
    global star_activity 
    if activity == "resting":
        if last_activity == "resting":
            duration += last_activity_duration
        if duration >= 120:
            tired = False
    elif activity == "running":
        effective_duration = 180
        if last_activity == "running":
            effective_duration = max(0,180 - last_activity_duration) 
        effective_duration = min(effective_duration,duration)*1
        cur_health += effective_duration * 3
        if (duration - effective_duration) > 0:
            cur_health += (duration - effective_duration)
        if tired:
            if star_activity != "running":
                cur_hedons-= 2 * duration
            else:
                cur_hedons+=min(duration, 10) * 1
                cur_hedons-=max(duration - 10, 0) * 2
        else:
            if star_activity != "running":
                cur_hedons += min(duration, 10) * 2 
            else:
                cur_hedons += min(duration, 10) * 5
            cur_hedons -= max(duration - 10, 0)* 2     
        tired = True
    elif activity == "textbooks":
        cur_health += duration * 2
        if tired:
            if star_activity != "textbooks":
                cur_hedons -= 2*duration
            else:
                cur_hedons += min(duration,10) * 1
                cur_hedons -= max(duration-10,0) * 2
        else:
            if star_activity != "textbooks":
                cur_hedons += min(duration,20) * 1 
            else:
                cur_hedons += min(duration,10) * 4
                if duration > 10:
                    cur_hedons += min(duration-10,10) * 1
            cur_hedons -= max(duration-20,0) * 1     
        tired = True
    else:
        return
    if last_activity != activity:
        last_activity = activity
        last_activity_duration = duration
    else:
        last_activity_duration += duration 
    update_star(duration)
    
def update_star(duration):
    global star_activity, star_num
    global star_list 
    
    star_activity = None 
    if not bored_with_stars:
        for i in range (star_num-1,-1,-1):
            star_list[i]-=duration
            if(star_list[i] <= 0):
                star_num -=1
    

def get_cur_hedons():
    return cur_hedons
    
def get_cur_health():
    return cur_health
    
def offer_star(activity):
    global star_activity
    global star_num 
    global star_list
    global bored_with_stars
    
    star_num += 1
    if star_num > 2 or bored_with_stars: #The user lose interests 
        star_activity = None #No more star_activity
        bored_with_stars = True
        return
    star_activity = activity
    star_list.insert(0, 120)

        
def most_fun_activity_minute():
    if star_activity != None:
        return star_activity
    if not tired :
        return "running"
    else:
        return "resting"

def run_test(actual, expected): 
    if expected == actual:
        return "passed"
    else:
        return "failed" 
    

##########################################################################
initialize()
if __name__ == '__main__':
    initialize()
    ######################################################################
    '''part 1: simples test without stars for single activity'''
    
    #test resting
    perform_activity("resting",10)
    print("Test 1:",run_test(get_cur_health(),0)) 
    print("Test 2:",run_test(get_cur_hedons(),0))         
    
    #test running without running over 180 minutes
    initialize()
    perform_activity("running", 180)#running exactly 180 minutes
    print("Test 3:",run_test(get_cur_health(),540)) 
    print("Test 4:",run_test(get_cur_hedons(),-320))        
    
    perform_activity("resting",10)#testing if the user is tired
    print("Test 5:",run_test(most_fun_activity_minute(),"resting"))  
     
    perform_activity("resting",109)#testing edge case when the user has rested for almost two hours but still tired
    print("Test 6:",run_test(most_fun_activity_minute(),"resting"))   
    perform_activity("resting",1)# testing edge case when the user has rested for just two hours and becomes not tired
    
    print("Test 7:",run_test(most_fun_activity_minute(),"running"))  
     
    perform_activity("running",30)
    perform_activity("running",150)#running exactly 180 minutes
    print("Test 8:",run_test(get_cur_health(),1080)) 
    print("Test 9:",run_test(get_cur_hedons(),-640))  
   
    #test running with running over 180 minutes
    initialize()
    perform_activity("running",181) #testing running just over 180 minutes(edge case)
    perform_activity("playing",1000)#testing anything other than running,resting and carrying textbooks should have no effect at all
    print("Test 10:",run_test(get_cur_health(),541)) 
    print("Test 11:",run_test(get_cur_hedons(),-322))   
          
    perform_activity("running",30)
    print("Test 12:",run_test(get_cur_health(),571)) 
    print("Test 13:",run_test(get_cur_hedons(),-382))         
    print("Test 14:",run_test(star_can_be_taken("running"),False))
    initialize()
    perform_activity("running",30)
    perform_activity("running",151) #testing running two times consecutively and over 180 minutes
    
    print("Test 15:",run_test(get_cur_health(),541)) 
    print("Test 16:",run_test(get_cur_hedons(),-322))          
   
    #test textbook carrying
    initialize() 
    print("Test 17:",run_test(most_fun_activity_minute(),"running"))
    perform_activity("textbooks",30)
    
    print("Test 18:",run_test(get_cur_health(),60)) 
    print("Test 19:",run_test(get_cur_hedons(),10))
    print("Test 20:",run_test(most_fun_activity_minute(),"resting"))#test if tired or not
    print("Test 21:",run_test(star_can_be_taken("textbooks"),False))#test star can be taken function
    
    

##########################################################################    
    '''part 2: tests involving multiple activities, but not stars'''
    initialize()
    perform_activity("running",10)     
    print("Test 22:",run_test(get_cur_health(),30)) 
    print("Test 23:",run_test(get_cur_hedons(),20))  
    perform_activity("textbooks", 30)#testing if it is tired(it should be)
        
    print("Test 24:",run_test(get_cur_health(),90)) 
    print("Test 25:",run_test(get_cur_hedons(),-40)) 
    print("Test 26:",run_test(most_fun_activity_minute(),"resting")) 
    
    perform_activity("resting", 30)    
    perform_activity("resting", 90)
    print("Test 27:",run_test(most_fun_activity_minute(),"running"))
    
    perform_activity("textbooks",20)#testing if it is not tired now(it should not be tired)
    print("Test 28:",run_test(get_cur_health(),130)) 
    print("Test 29:",run_test(get_cur_hedons(),-20))    
    
    perform_activity("running",300)
    print("Test 24:",run_test(get_cur_health(),790)) 
    print("Test 25:",run_test(get_cur_hedons(),-620))   
    
    perform_activity("resting",119)#testing if it is tired(it should be) when it almost will become not tired(edge case)
    perform_activity("textbooks", 20)    
    print("Test 26:",run_test(get_cur_health(),830)) 
    print("Test 27:",run_test(get_cur_hedons(),-660)) 
       
    perform_activity("resting",120)#testing if it is not tired now(it should not be tired)
    perform_activity("running", 11)    
    print("Test 28:",run_test(get_cur_health(),863)) 
    print("Test 29:",run_test(get_cur_hedons(),-642))   
     
    perform_activity("running",170)  #testing running consecutively over 180 minutes
    print("Test 36:",run_test(get_cur_health(),1371)) 
    print("Test 37:",run_test(get_cur_hedons(),-982)) 
    
    
    
##########################################################################    
    '''part 3: tests offering of stars'''
    initialize()
    #testing when no stars are offered
    print("Test 38:",run_test(star_can_be_taken("runnning"),False))
    print("Test 39:",run_test(star_can_be_taken("textbooks"),False))
    print("Test 40:",run_test(star_can_be_taken("resting"),False))
    print("Test 41:",run_test(most_fun_activity_minute(),"running"))
    
    #testing when a star is offered for running
    offer_star("running")
    print("Test 42:",run_test(star_can_be_taken("running"),True))
    print("Test 43:",run_test(star_can_be_taken("textbooks"),False))
    print("Test 44:",run_test(star_can_be_taken("resting"),False))
    print("Test 45:",run_test(most_fun_activity_minute(),"running"))
    
    initialize()
    #testing when a star is offered for carrying textbooks
    offer_star("textbooks")
    print("Test 46:",run_test(star_can_be_taken("running"),False))
    print("Test 47:",run_test(star_can_be_taken("textbooks"),True))
    print("Test 48:",run_test(star_can_be_taken("resting"),False))
    print("Test 49:",run_test(most_fun_activity_minute(),"textbooks")) 
    
    
    
##########################################################################    
    '''part 4: tests involving stars for running'''
    initialize()
    offer_star("running")
    perform_activity("running",5)#testing extra hedons  
    perform_activity("running",5)#no more extra hedons
    print("Test 50:",run_test(get_cur_health(),30)) 
    print("Test 51:",run_test(get_cur_hedons(),15))    
    
    offer_star("running")
    perform_activity("running",109)#testing running with stars but tired
    print("Test 52:",run_test(get_cur_health(),357)) 
    print("Test 53:",run_test(get_cur_hedons(),-173))
    
    offer_star("running")#testing three stars offered within exactly in the span of 2 hours(edge case)
    perform_activity("running",61)
    print("Test 54:",run_test(get_cur_health(),540))#total running time is 180 minutes, meaning that 3 health points are given every minute
    print("Test 55:",run_test(get_cur_hedons(),-295))#bored with stars now
    offer_star("running")#testing if stars are still ineffective
    perform_activity("running",200)
    print("Test 56:",run_test(get_cur_health(),740)) #these 200 minutes should all give 1 health point per minute
    print("Test 57:",run_test(get_cur_hedons(),-695))
    
    initialize()
    offer_star("running")
    perform_activity("running",11)#testing performing star activity for more than 10 minutes and not tired
    print("Test 58:",run_test(get_cur_health(),33)) 
    print("Test 59:",run_test(get_cur_hedons(),48))  
      
    offer_star("running")
    perform_activity("running",109)#testing running with stars but tired
    print("Test 60:",run_test(get_cur_health(),360)) 
    print("Test 61:",run_test(get_cur_hedons(),-140))
    
    offer_star("running")#testing three stars offered just outside of a span of 2 hours(edge case)
    perform_activity("running",9)#testing extra hedons for less than 10 minutes
    print("Test 62:",run_test(get_cur_health(),387)) 
    print("Test 63:",run_test(get_cur_hedons(),-131))
 
 
 
##########################################################################   
    '''part 5: tests involving stars for carrying textbooks'''
    initialize()
    offer_star("textbooks")
    perform_activity("textbooks",20)#testing carrying textbooks for 20 minutes when a star is offered for carrying textbooks and not tired
    print("Test 64:",run_test(get_cur_health(),40)) 
    print("Test 65:",run_test(get_cur_hedons(),50)) 
       
    offer_star("textbooks")
    perform_activity("textbooks",5)#extra hedons
    perform_activity("textbooks",94)#no more extra hedons
    print("Test 66:",run_test(get_cur_health(),238)) 
    print("Test 67:",run_test(get_cur_hedons(),-133))
    
    offer_star("textbooks")#testing three stars offered within exactly in the span of 2 hours(edge case)
    perform_activity("textbooks",10)#bored with stars now
    print("Test 68:",run_test(get_cur_health(),258)) 
    print("Test 69:",run_test(get_cur_hedons(),-153))
    
    offer_star("textbooks")#stars are still ineffective
    perform_activity("textbooks",10)
    print("Test 70:",run_test(get_cur_health(),278)) 
    print("Test 71:",run_test(get_cur_hedons(),-173))#tired and no extra hedons
    
    initialize()
    offer_star("textbooks")
    perform_activity("textbooks",10)#testing performing star activity for less than 20 minutes and not tired
    print("Test 72:",run_test(get_cur_health(),20)) 
    print("Test 73:",run_test(get_cur_hedons(),40))   
     
    offer_star("textbooks")#test carrying textbooks when tired
    perform_activity("textbooks",110)
    print("Test 74:",run_test(get_cur_health(),240)) 
    print("Test 75:",run_test(get_cur_hedons(),-150))
    
    offer_star("textbooks")#testing three stars offered just outside of a span of 2 hours(edge case)
    perform_activity("textbooks",9)#testing carrying textbooks for less than 20 minutes when tired and stars are offered
    print("Test 76:",run_test(get_cur_health(),258)) 
    print("Test 77:",run_test(get_cur_hedons(),-141)) 
 
 
    
##########################################################################
    '''part 6: tests involving stars for multiple activities'''
    initialize()
    offer_star("running")  
    perform_activity("resting",70)#testing performing activity is not offer star activity
    print("Test 78:",run_test(get_cur_health(),0)) 
    print("Test 79:",run_test(get_cur_hedons(),0))   
    
    offer_star("textbooks")
    perform_activity("textbooks",50)#testing carrying textbooks for more than 20 minutes when star is offered and not tired
    print("Test 80:",run_test(get_cur_health(),100)) 
    print("Test 81:",run_test(get_cur_hedons(),20))
    
    offer_star("running")#testing three stars offered just outside a span of 2 hours(edge case)
    perform_activity("running",50)
    print("Test 82:",run_test(get_cur_health(),250)) 
    print("Test 83:",run_test(get_cur_hedons(),-50))
    
    perform_activity("resting",20)          
    offer_star("textbooks")#testing three stars offered just outside a span of 2 hours again!
    print("Test 84:",run_test(star_can_be_taken("textbooks"),True))
    print("Test 85:",run_test(most_fun_activity_minute(),"textbooks"))
    
    perform_activity("textbooks",11)#testing carrying textbooks for more than the duratino of bonus hedon(edge case)
    print("Test 86:",run_test(get_cur_health(),272)) 
    print("Test 87:",run_test(get_cur_hedons(),-42))
    
    perform_activity("resting",120)#testing resting for just the enough time to become not tired
    print("Test 88:",run_test(most_fun_activity_minute(),"running"))
    
    offer_star("textbooks")#testing perform activity is running but offer star activity is textbooks
    perform_activity("running",5)#no bonus hedons,not tired
    perform_activity("running",5)#no bonus hedons,tired
    print("Test 89:",run_test(get_cur_health(),302)) 
    print("Test 90:",run_test(get_cur_hedons(),-42)) 
    
    offer_star("running")
    perform_activity("textbooks",110)#no bonus hedons because star activity is running not carrying textbooks 
    print("Test 91:",run_test(get_cur_health(),522)) 
    print("Test 92:",run_test(get_cur_hedons(),-262))  
    
    offer_star("textbooks")#testing three stars offered just outside a span of 2 hours again!
    print("Test 93:",run_test(star_can_be_taken("running"),False))
    print("Test 94:",run_test(star_can_be_taken("textbooks"),True))
    
    perform_activity("resting",9)
    offer_star("running")#stars are ineffective
    print("Test 95:",run_test(star_can_be_taken("running"),False))
    
    perform_activity("resting",120)
    perform_activity("playing",1000)#testing something other than resting, textbooks, and running should not have any effect.
    offer_star("running")#bored with star
    perform_activity("running",10)#testing running when not tired and bored with star for just 10 minutes(edge case for gaining hedons)
    print("Test 96:",run_test(get_cur_health(),552)) 
    print("Test 97:",run_test(get_cur_hedons(),-242))
    
    perform_activity("running",171)#testing running when bored with stared, tired and running over 180 minutes 
    print("Test 98:",run_test(get_cur_health(),1063)) 
    print("Test 99:",run_test(get_cur_hedons(),-584)) 
    
    perform_activity("resting",120)
    offer_star("textbooks")
    perform_activity("textbooks",20)#testing carrying textbooks when not tired and bored with star for just 20 minutes(edge case for gaining hedons)
    print("Test 100",run_test(get_cur_health(),1103))
    print("Test 101",run_test(get_cur_hedons(),-564))
 