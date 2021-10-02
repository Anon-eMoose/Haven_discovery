define battle_narrator = Character(None, interact=False)
screen battle_screen:
    vbox:
        xalign 0.01 yalign 0.1
        spacing 5
        
        for each_party_member in party_list:
            frame:
                size_group "party"
                xminimum 250 xmaximum 250
                yminimum 75
                vbox:
                    text "[each_party_member[name]]" size 22 xalign 0.5
                    null height 5
                    hbox:
                        bar:
                            xmaximum 130
                            value each_party_member["current_hp"]
                            range each_party_member["max_hp"]
                            left_gutter 0
                            right_gutter 0
                            thumb None
                            thumb_shadow None
                            left_bar Frame("gui/barfull.png", 10, 0)
                            right_bar Frame("gui/barempy.png", 10, 0)
                        null width 5
                        if each_party_member["current_hp"] <=0:
                         text "KO'd" size 16
                        else:
                         text "[each_party_member[current_hp]] / [each_party_member[max_hp]]" size 16
        
        hbox:
            frame:
                size_group "party"
                yminimum 40
                text "Medipacks [potions_left]" yalign 0.0 xalign 0.5 size 22
            if players_turn and potions_left > 0:
                textbutton "<- Use" action Return("heal") yminimum 30
            else:
                textbutton "<- Use" action None yminimum 30
        
    vbox:
        xalign 0.90 yalign 0.1
        spacing 5
        
        if enemies_list != []:
            for i, each_enemy_member in enumerate(enemies_list):
                hbox:
                    if players_turn and each_enemy_member["current_hp"] > 0:
                        textbutton "Attack ->" action Return(i) yminimum 75
                    else:
                        textbutton "Attack ->" action None yminimum 75
                    
                    frame:
                        size_group "enemies"
                        xminimum 250 xmaximum 250
                        yminimum 75
                        vbox:
                            text "[each_enemy_member[name]]" size 22 xalign 0.5
                            null height 5   
                            hbox:
                                bar:
                                    xmaximum 130
                                    value each_enemy_member["current_hp"]
                                    range each_enemy_member["max_hp"]
                                    left_gutter 0
                                    right_gutter 0
                                    thumb None
                                    thumb_shadow None
                                    left_bar Frame("gui/barfull.png", 10, 0)
                                    right_bar Frame("gui/barempy.png", 10, 0) 
                                null width 5
                                
                                text "[each_enemy_member[current_hp]] / [each_enemy_member[max_hp]]" size 16
 
init python:
    def check_party(x):
        #### This function will check
        # if at least one of X party members is alive.
        #        
        for member in x:
            if member["current_hp"] > 0:
                return "ok"
                
        return "lost"



label battle_game_3:
    show bg cave6
    hide screen inventory
    hide screen itemdisplay
    #### Some variables that describes the game state.
    #
    # The "party_list" is a list of all allies each one of that
    # is described by a dictionary.
    #
    $ party_list =[{"name":"Eebee", "max_hp":100, "current_hp":healthcount, "min_damage":3, "max_damage":5}]
    $ potions_left = 10
    $ players_turn = False
    
    #### Enemies list will have the description for enemies.
    $ enemies_list = []
    
   
## show the game screen.
    show screen battle_screen

   ##Load in eebee health graphics##
    if healthcount <=50:
        show eebee idle50 at Position (xalign = 0.00, yalign = 0.648) with dissolve:
         xzoom 0.3 yzoom 0.3
    elif healthcount >=51:
        show eebee idle100 at Position (xalign = 0.00, yalign = 0.648) with dissolve:
         xzoom 0.3 yzoom 0.3
 
   ##Load in oleka health graphics##
    if olekahealth <=50:
        show oleka idle50 at Position (xalign = 0.02, yalign = 0.648) with dissolve:
         xzoom 0.3 yzoom 0.3
    elif olekahealth >=51:
        show oleka idle100 at Position (xalign = 0.02, yalign = 0.648) with dissolve:
         xzoom 0.3 yzoom 0.3
 
    ##Load in Blazer health graphics##
    if blazerhealth <=50:
        show blazer idle50 at Position (xalign = 0.02, yalign = 0.540) with dissolve:
         xzoom 0.3 yzoom 0.3
    elif blazerhealth >=51:
        show blazer idle100 at Position (xalign = 0.02, yalign = 0.540) with dissolve:
         xzoom 0.3 yzoom 0.3

    show ponipede idle  at Position (xalign = 0.5, yalign = -0.8) with dissolve
## We can add some allies to the party:##
    menu:
        "Malicious code dectected"
        "Help AI":
            $ party_list.append ( {"name":"Oleka", "max_hp":100, "current_hp":olekahealth, "min_damage":5, "max_damage":6} )
            $ party_list.append ( {"name":"Blazer", "max_hp":100, "current_hp":blazerhealth, "min_damage":10, "max_damage":15} )
            play music "audio/music/suspended-battle.ogg"
    
## Enemies party can be set manually or automatically like:##
            $ enemies_list.append ( {"name":"P0niP3d3", "max_hp":500, "current_hp":500, "min_damage":10, "max_damage":20} )          
    "Let the battle begin!"

## Main battle loop.##
    label battle_3_loop:

## At first let's check if player's party is ok.##
        if check_party(party_list) == "lost":
            jump battle_3_lose     
        
        #### All the party members will do their actions one after another.
        $ party_index = 0
        
        while party_index < len(party_list):
            
            $ current_player = party_list[party_index]
            
            #### Current player will act only if he still alive.
            #
            if current_player["current_hp"] > 0:
                
                #### Let's check if enemies party is still ok.
                #
               if check_party(enemies_list) == "lost":
                jump battle_2_win
            
                #### Let the player make his turn.
                #
               label playerturn2:
                $ players_turn = True
                
                if current_player["name"] == 'Eebee':
                 if healthcount <=50:
                  show eebee idle50 at Position (xalign = 0.07, yalign = 0.642) with dissolve
                 elif healthcount >=51:
                  show eebee idle100 at Position (xalign = 0.07, yalign = 0.642) with dissolve
                
                elif current_player["name"] == 'Oleka':
                 if olekahealth <=50:
                  show oleka idle50 at Position (xalign = 0.07, yalign = 0.642) with dissolve
                 elif olekahealth >=51:
                  show oleka idle100 at Position (xalign = 0.07, yalign = 0.642) with dissolve
                show ponipede idle
                battle_narrator"[current_player[name]], it's your turn now."
                
                #### Store the result of player's interaction.
                #
               $ res = ui.interact()
                
                #### Now disallow player's interact with the game.
                #
               $ players_turn = False
               if res == "heal":
                   if current_player["name"] == 'Eebee':
                    $ current_player["current_hp"] = min( current_player["current_hp"]+10, current_player["max_hp"] )
                    $ potions_left -= 1
                    $ healthcount += 10
                    show eebee heal at Position (xalign = 0.07, yalign = 0.645) with dissolve
                    e "10hp restored"
                   elif current_player["name"]  == 'Oleka':
                    $ current_player["current_hp"] = min( current_player["current_hp"]+10, current_player["max_hp"] )
                    $ potions_left -= 1
                    $ olekahealth += 10
                    show oleka heal at Position (xalign = 0.07, yalign = 0.642) with dissolve
                    o "10hp restored"
                   elif current_player["name"]  == 'Blazer':
                    $ current_player["current_hp"] = min( current_player["current_hp"]+10, current_player["max_hp"] )
                    $ potions_left -= 1
                    $ blazerhealth += 10
                    show oleka heal at Position (xalign = 0.07, yalign = 0.642) with dissolve
                    b "10hp restored"
               else:
                $ player_damage = renpy.random.randint( current_player["min_damage"], current_player["max_damage"] )
                $ enemies_list[res]["current_hp"] -= player_damage
                if current_player["current_hp"] <= 0:
                 "Take this! (damage dealt - [player_damage]hp)"
                else:
                 if current_player["name"] == 'Eebee':
                  show eebee fight at Position (xalign = 0.07, yalign = 0.642) with dissolve:
                   xzoom 0.3 yzoom 0.3
                  show ponipede hurt
                  call expression renpy.random.choice(["etaunt1", "etaunt2", "etaunt3"]) from _call_expression_2
                  
                 elif current_player["name"] == 'Oleka':
                  show oleka fight at Position (xalign = 0.07, yalign = 0.642) with dissolve:
                   xzoom 0.3 yzoom 0.3
                  show ponipede hurt
                  call expression renpy.random.choice(["otaunt1", "otaunt2", "otaunt3"]) from _call_expression_3
                  
                 elif current_player["name"] == 'Blazer':
                  show blazer attack at Position (xalign = 0.07, yalign = 0.642) with dissolve:
                   xzoom 0.3 yzoom 0.3
                  show ponipede hurt
                  call expression renpy.random.choice(["btaunt1", "btaunt2", "btaunt3"]) from _call_expression_4
                    
            ## And the turn goes to the next party member.##
            label battle_cont2:
            $ party_index += 1
            if current_player["name"] == 'Eebee':
                if healthcount <=50:
                 show eebee idle50  at Position (xalign = 0.00, yalign = 0.648) with dissolve
                elif healthcount >=51:
                 show eebee idle100 at Position (xalign = 0.00, yalign = 0.648) with dissolve
                
            elif current_player["name"] == 'Oleka':
                if healthcount <=50:
                 show oleka idle50 at Position (xalign = 0.00, yalign = 0.648) with dissolve
                elif healthcount >=51:
                 show oleka idle100 at Position (xalign = 0.00, yalign = 0.648) with dissolve
                    
            elif current_player["name"] == 'Blazer':
                if healthcount <=50:
                 show blazer idle50 at Position (xalign = 0.00, yalign = 0.540) with dissolve
                elif healthcount >=51:
                 show blazer idle100 at Position (xalign = 0.00, yalign = 0.540) with dissolve
            
        ## And now it's enemies party turn.##
        
        ## At first let's check if enemy's party is ok.##
        
        if check_party(enemies_list) == "lost":
            hide snaike fight
            jump battle_2_win
        
        
        
        ## All the party members will do their actions one after another.
        $ enemy_index = 0
        
        while enemy_index < len(enemies_list):
            $ current_enemy = enemies_list[enemy_index]
            
            ## Current enemy will act only if he is still alive.
            
            if current_enemy["current_hp"] > 0:
                
                ## Let's check if player's party is still ok.
                if check_party(party_list) == "lost":
                    jump battle_3_lose
                
                ## Enemy will attack the random player.
                
                $ party_member_to_attack = party_list[renpy.random.randint( 0, (len(party_list)-1) )]

                $ enemy_damage = renpy.random.randint( current_enemy["min_damage"], current_enemy["max_damage"] )
                
                $ party_member_to_attack["current_hp"] -= enemy_damage
                ##Eebees Hit##
                if party_member_to_attack["name"] == "Eebee":
                 if party_member_to_attack["current_hp"] <= 0:
                  show ponipede attack
                  show eebee ko at Position (xalign = 0.00, yalign = 0.648) with dissolve
                  "([current_enemy[name]] continues to attack [party_member_to_attack[name]])!"
                  $ healthcount = 1
                 else:
                  show ponipede attack
                  show eebee hurt at Position (xalign = 0.00, yalign = 0.648) with dissolve
                  "tewst Rrrrr! ([current_enemy[name]] dealt [enemy_damage]hp damage to [party_member_to_attack[name]])"
                  $ healthcount -= enemy_damage
                ##Oleka Hit##
                elif party_member_to_attack["name"] == "Oleka":
                 if party_member_to_attack["current_hp"] <= 0:
                  show ponipede attack
                  show oleka hurt at Position (xalign = 0.02, yalign = 0.648) with dissolve
                  "([current_enemy[name]] continues to attack [party_member_to_attack[name]])!"
                  $ olekahealth = 1
                 else:
                  show ponipede attack
                  show oleka hurt at Position (xalign = 0.02, yalign = 0.648) with dissolve
                  $ olekahealth -= enemy_damage
                  "Rrrrr! ([current_enemy[name]] dealt [enemy_damage]hp damage to [party_member_to_attack[name]])"  
                elif party_member_to_attack["name"] == "Blazer":
                 if party_member_to_attack["current_hp"] <= 0:
                  show ponipede attack
                  show oleka hurt at Position (xalign = 0.02, yalign = 0.648) with dissolve
                  "([current_enemy[name]] continues to attack [party_member_to_attack[name]])!"
                  $ olekahealth = 1
                 else:
                  show ponipede attack
                  show oleka hurt at Position (xalign = 0.02, yalign = 0.648) with dissolve
                  $ olekahealth -= enemy_damage
                  "blazer hurt Rrrrr! ([current_enemy[name]] dealt [enemy_damage]hp damage to [party_member_to_attack[name]])"  
            ## And the turn goes to the next party member.
            
            $ enemy_index += 1
            
            
        ## Next round of the battle.
    if healthcount <=50:
        show eebee idle50 at Position (xalign = 0.00, yalign = 0.648) with dissolve
    elif healthcount >=51:
        show eebee idle100 at Position (xalign = 0.00, yalign = 0.648) with dissolve
    
    if olekahealth <=50:
        show oleka idle50 at Position (xalign = 0.02, yalign = 0.648) with dissolve
    elif olekahealth >=51:
        show oleka idle100 at Position (xalign = 0.02, yalign = 0.648) with dissolve
        
    if blazerhealth <=50:
        show blazer idle50 at Position (xalign = 0.02, yalign = 0.540) with dissolve:
    elif blazerhealth >=51:
        show blazer idle100 at Position (xalign = 0.02, yalign = 0.540) with dissolve:
    
    jump battle_3_loop
            
            
## The results of the game.

label battle_3_win:
    show snaike death at Position (xpos=0.85, xanchor=0.5, ypos=0.9, yanchor=0.5) 
    "Well done!"
    hide snaike death
    $ cryptocount += 35
    "+35 Crypto's found"
    $ inv.append("cube")
    "+1 Artifact found"
    pause
    hide screen battle_screen
    return
    
label battle_3_lose:
    "X_X"
    hide screen battle_screen
    return