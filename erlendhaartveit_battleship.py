# Battleship

# En spiller mot en AI motstander.
# Hver spiller har et rutenett.
# Hver spiller har ruter som representerer et eller flere battleships.
# Hver spiller tar tur for å treffe en rute (et skip).
# Når en spiller har "mistet" alle sine battleships, har den andre spilleren vunnet.

# -3: Skip 2 skutt, osv...
# -2: Skip 1 skutt
# -1: Skutt vann
# 1: Uskutt vann
# 2: Skip 1
# 3: Skip 2, osv...

# [
#  [1,1,1],
#  [1,2,1],
#  [1,2,1],
#  [1,1,1]
#  ]

small_ship_size=2
medium_ship_size=3
large_ship_size=4

# default boat settings.
# b_small=1
# b_medium=0
# b_large=0
# sigh, error? :/ Put in a list then?...
ships=[1,0,0]

# def set_ship_count(x,y,z):
#     b_small=x
#     b_medium=y
#     b_large=z

# SETS THE DIMENSION OF THE MAP.

# Default map dimensions.
map_dimensions=[3,4]
# map_dimensions=[3,5] # works!
# Okay... So we would like to create: (btw, doesn't give error when uncommented)
[
 [1,1,1],
 [1,1,1],
 [1,1,1],
 [1,1,1]
 ]

map_size=map_dimensions[0]*map_dimensions[1]

game_map=[]

row_list=[]
for x in range(map_dimensions[0]):
    row_list.append(1)

#print(row_list) # [1, 1, 1]

for y in range(map_dimensions[1]):
    game_map.append(row_list)

def get_pos_val(x,y):
    return game_map[y][x] 

import random
y_length=len(game_map)
row_length=len(row_list)

# Hm... Try to make a dictionary instead?...
map_dict={}
ai_map_dict={}

for y in range(y_length):
    list_item=game_map[y]
    #print(list_item) # [1, 1, 1]
    item_length=len(list_item)
    for x in range(item_length):
        map_dict[x,y]=1
        ai_map_dict[x,y]=1
        #map_dict[point]=1

#print(map_dict)

small_boat_locations=[]
medium_boat_locations=[]
large_boat_locations=[]

ai_small_locations=[]
ai_medium_locations=[]
ai_large_locations=[]

# Ex. for small ship -> size==2, for each point, checks only 1 point forward/down.
# Hm, just ran once in the start, so... Same for AI too then? Same map size.
def get_possible_ships(size,location_list):
    steps=size-1
    #print(steps)
    for y in range(y_length):
        for x in range(row_length):
            cur_point=(x,y)
            right_points_exist=True
            right_points=[]
            right_points.append(cur_point)
            for step_right in range(steps):
                step_right+=1
                point_right=(x+step_right,y)
                right_points.append(point_right)
                if not point_right in map_dict:
                    right_points_exist=False
                    break
            if right_points_exist:
               # at this point, the point(s) should exist.
                location_list.append(right_points)
            
            down_points_exist=True
            down_points=[]
            down_points.append(cur_point)
            for step_down in range(steps):
                step_down+=1
                point_down=(x,y+step_down)
                down_points.append(point_down)
                if not point_down in map_dict:
                    down_points_exist=False
                    break
            if down_points_exist:
                location_list.append(down_points)

get_possible_ships(2,small_boat_locations) # len: 17
get_possible_ships(3,medium_boat_locations) # len: 10
get_possible_ships(4,large_boat_locations)  # len: 3

get_possible_ships(2,ai_small_locations)
get_possible_ships(3,ai_medium_locations)
get_possible_ships(4,ai_large_locations)

def get_used_positions(map_dictionary):
    used_points=[]
    for y in range(y_length):
        for x in range(row_length):
            cur_point=(x,y)
            value=map_dictionary[cur_point]
            if value<=0 or value>1:
                used_points.append(cur_point)
    return used_points

def update_boat_locations(boat_list,map_dictionary):
    used_points=get_used_positions(map_dictionary)
    used_points_length=len(used_points)
    #print(used_points_length) # 0
    for index in range(used_points_length):
        used_point=used_points[index]
        # alright, gotta use a backward loop to delete list items:
        boats_len=len(boat_list)-1
        for boat_index in range(boats_len,-1,-1):
            boat=boat_list[boat_index]
            #print(boat)
            boat_l=len(boat)
            boat_point_used=False
            for point_index in range(boat_l):
                point=boat[point_index]
                if point==used_point:
                    boat_point_used=True
                    break
            if boat_point_used:
                del boat_list[boat_index]

def update_all_locations(map_dictionary):
    update_boat_locations(small_boat_locations,map_dictionary)
    update_boat_locations(medium_boat_locations,map_dictionary)
    update_boat_locations(large_boat_locations,map_dictionary)
    
def update_locations(small_loc,medium_loc,large_loc,map_dictionary):
    update_boat_locations(small_loc,map_dictionary)
    update_boat_locations(medium_loc,map_dictionary)
    update_boat_locations(large_loc,map_dictionary)

player_boats={"small":[],"medium":[],"large":[]}
ai_boats={"small":[],"medium":[],"large":[]}

# Hm... Is this a bit redundant? :/ ...
# Sigh, just keep for now.
fleet={"boats":0,"areas":0,"small":0,"medium":0,"large":0}
ai_fleet={"boats":0,"areas":0,"small":0,"medium":0,"large":0}

def create_boat(small,medium,large,team,small_locations,medium_locations,large_locations,map_dictionary):
    for index in range(small):
        boat_locations=len(small_locations)
        #print(f"small ~ boat_locations: {boat_locations}")
        if boat_locations>0:
            random_location=random.randint(0,boat_locations-1)
            boat=small_locations[random_location]
            if team==0:
                player_boats["small"].append(boat)
                #print(f"player ~ boat: {boat}")
            else:
                ai_boats["small"].append(boat)
                #print(f"ai ~ boat: {boat}")
            boat_l=len(boat)
            for p in range(boat_l):
                point=boat[p]
                map_dictionary[point]=2
            update_locations(small_locations,medium_locations,large_locations,map_dictionary)
        else:
            print("No more room for a small ship!")
        
    for index in range(medium):
        boat_locations=len(medium_locations)
        #print(f"medium ~ boat_locations: {boat_locations}")
        if boat_locations>0:
            random_location=random.randint(0,boat_locations-1)
            boat=medium_locations[random_location]
            if team==0:
                player_boats["medium"].append(boat)
            else:
                ai_boats["medium"].append(boat)
            boat_l=len(boat)
            for p in range(boat_l):
                point=boat[p]
                map_dictionary[point]=3
            update_locations(small_locations,medium_locations,large_locations,map_dictionary)
        else:
            print("No more room for a medium ship!")
            
    for index in range(large):
        boat_locations=len(large_locations)
        #print(f"large ~ boat_locations: {boat_locations}")
        if boat_locations>0:
            random_location=random.randint(0,boat_locations-1)
            boat=large_locations[random_location]
            if team==0:
                player_boats["large"].append(boat)
            else:
                ai_boats["large"].append(boat)
            boat_l=len(boat)
            for p in range(boat_l):
                point=boat[p]
                map_dictionary[point]=4
            update_locations(small_locations,medium_locations,large_locations,map_dictionary)
        else:
            print("No more room for a large ship!")

def add_boats(small,medium,large,team):
    boat_count=0
    if small<0:
        small=0
    if medium<0:
        medium=0
    if large<0:
        large=0
    boat_count=(small+medium+large)
    if boat_count==0:
        print("At least 1 boat needs to be added.")
        pass
    
    if team==0:
        create_boat(small,medium,large,team,small_boat_locations,medium_boat_locations,large_boat_locations,map_dict)
    else:
        create_boat(small,medium,large,team,ai_small_locations,ai_medium_locations,ai_large_locations,ai_map_dict)
    
player=0
ai=1

# ADDING BOATS TO THE GAME.

#add_boats(1,0,0,player)
#add_boats(2,0,0,player) # works!
#print(map_dict)

#add_boats(1,0,0,ai)
#add_boats(2,0,0,ai)
#print(ai_map_dict)

def count_boats_remaining(team):
    boat_count=0
    areas=0
    small=0
    medium=0
    large=0
    if team==0:
        for t in player_boats.keys():
            #print(t)
            boats=len(player_boats[t])
            for index in range(boats):
                #print(player_boats[t][index])
                area_l=len(player_boats[t][index])
                if area_l>0:
                    boat_count+=1
                    if t=="small":
                        small+=1
                    elif t=="medium":
                        medium+=1
                    else:
                        large+=1
                    #area_l=len(player_boats[t][index])
                    for area in range(area_l):
                        areas+=1
        fleet["boats"]=boat_count
        fleet["areas"]=areas
        fleet["small"]=small
        fleet["medium"]=medium
        fleet["large"]=large
    else:
        for t in ai_boats.keys():
            #print(t)
            boats=len(ai_boats[t])
            for index in range(boats):
                #print(ai_boats[t][index])
                area_l=len(ai_boats[t][index])
                #print(area_l)
                if area_l>0:
                    boat_count+=1
                    if t=="small":
                        small+=1
                    elif t=="medium":
                        medium+=1
                    else:
                        large+=1
                        #area_l=len(ai_boats[t][index])
                    for area in range(area_l):
                        areas+=1
        #print(f"boat_count: {boat_count}")
        #print(f"areas: {areas}")
        ai_fleet["boats"]=boat_count
        ai_fleet["areas"]=areas
        ai_fleet["small"]=small
        ai_fleet["medium"]=medium
        ai_fleet["large"]=large

# Next is...
# Starting the game. For each turn, choosing one point to "fire" at.
# When fired -> change value of the point.
# Also report whether it was a hit...
# And if all ships are down -> Announce victory / loss.

# note: ship points are saved in: player_boats, and ai_boats.
# Hm, I changed it to a dictionary ~ so can know whether what ship size each point belongs to.
#print(player_boats) # {'small': [[(0, 1), (1, 1)]], 'medium': [], 'large': []}
#print(ai_boats) # {'small': [[(1, 3), (2, 3)]], 'medium': [], 'large': []}
#print(len(player_boats["small"])) # 

numbers=0
for number in str(map_size):
    numbers+=1

lx="Lx"
mx="Mx"
sx="Sx"
xes=""
oes=""
ses=""
mes=""
les=""
for n in range(numbers):
    xes+="X"
    oes+="O"
    ses+="S"
    mes+="M"
    les+="L"
    if n>1:
        lx+="x"
        mx+="x"
        sx+="x"

def print_map(team):
    text="\n"
    
    for y in range(y_length):
        line=""
        for x in range(row_length):
            point=(x,y)
            value=0
            if team==0:
                value=map_dict[point]
            else:
                value=ai_map_dict[point]
            symbol=""
            if value==-4:#large ship
                symbol=lx
            elif value==-3:
                symbol=mx
            elif value==-2:
                symbol=sx
            elif value==-1:
                symbol=xes
            elif value==1:
                symbol=oes
            elif value==2:
                symbol=ses
            elif value==3:
                symbol=mes
            elif value==4:
                symbol=les
            line+=symbol+"  "
        #if not y==y_length-1:
        #    line+="\n"
        line+="\n"
        text+=line
    print(text)

#print_map(map_dict) # works?!
#print_map(player)

def remove_ship_point(point,team):
    if team==0:
        for t in player_boats.keys():
            #print(t)
            boats=len(player_boats[t])
            for index in range(boats):
                #print(player_boats[t][index])
                boat_l=len(player_boats[t][index])
                for i in range(boat_l):
                    boat_point=player_boats[t][index][i]
                    #print(boat_point)
                    #print(player_boats[t][index][boat_point])
                    if point==boat_point:
                        del player_boats[t][index][i]
                        #print(f"deleting point {point} from player_boats.")
                        return # need to return to avoid crash...
    else:
        for t in ai_boats.keys():
            #print(t)
            boats=len(ai_boats[t])
            for index in range(boats):
                #print(ai_boats[t][index])
                boat_l=len(ai_boats[t][index])
                for i in range(boat_l):
                    boat_point=ai_boats[t][index][i]
                    #print(boat_point)
                    if point==boat_point:
                        del ai_boats[t][index][i]
                        #print(f"deleting point {point} from ai_boats.")
                        return # need to return to avoid crash...

# Hm, create an "attack" map.
def create_attack_map(team,r):
    text="Choose an area to attack:\n\n"
    area_dict={}
    area_numbers=[]
    
    counter=0
    for y in range(y_length):
        line=""
        for x in range(row_length):
            counter+=1
            point=(x,y)
            value=0
            if team==0:
                value=ai_map_dict[point]
            else:
                value=map_dict[point]
            symbol=""
            if value<1:
                if value==-4:#large ship
                    symbol=lx
                elif value==-3:
                    symbol=mx
                elif value==-2:
                    symbol=sx
                else:
                    symbol=xes
            else:
                symbol=f'{counter:0{numbers}}'
                area_dict[counter]=point
                area_numbers.append(counter)
            line+=symbol+"  "
        if not y==y_length-1:
            line+="\n"
        text+=line
    
    if team==0:
        print(text)
    
    ai_ships_before=0
    player_hit_target=False
    ai_hit_target=False
    
    target=0
    if team==0:
        target=input("Area code: ")
        
        if target.isdigit():
            number=int(target)
            # Do a check first...
            #print(area_dict)
            if not number in area_dict:
                print("")
                print(f"Area code {target} is not valid. Please try again.")
                print("")
                create_attack_map(team)
                return
            #number=int(target)
            #print(number) # Ok, so 01 becomes 1.
            point=area_dict[number]
            #print(point) # (1,0)
            value=ai_map_dict[point]
            #print(value)
            if value==1:
                ai_map_dict[point]=-1
            elif value==2:
                ai_map_dict[point]=-2
            elif value==3:
                ai_map_dict[point]=-3
            else:
                ai_map_dict[point]=-4
            
            if value>1:
                print("")

                player_hit_target=True
                ai_ships_before=ai_fleet["boats"]
                remove_ship_point(point,ai)

        else:
            print("")
            print("Please type a valid area number.")
            print("")
            create_attack_map(team)
            return
        
        r+=1
              
        print(f'''
===============================================================================
ROUND: {r}
===============================================================================
              ''')

        if player_hit_target:
            count_boats_remaining(ai)
            ai_ships_now=ai_fleet["boats"]
            #print("")
            if ai_ships_now<=0:
                print("You've sunk the enemy fleet, congratulations!")
                return
            elif ai_ships_before>ai_ships_now:
                print("You've sunk a ship! Well done!")
            else:
                print("You hit an enemy ship!")
            print("")

        print(f'''The enemy launched an attack!
              ''')
              
        # Hm. Make AI attack!
        create_attack_map(ai,r)
        
        # Check for hit?
        count_boats_remaining(player)
        
        ships_now=fleet["boats"]
        if ships_now<=0:
            print("Your fleet has been sunk, unfortunately!")
            print("")
            return

        print(f'''Your fleet. Ships remaining: {fleet["boats"]}''')
        print_map(player)
        create_attack_map(team,r)
        
    else:

        player_areas=len(area_numbers)
        random_area=random.randint(0,player_areas-1)
        target=area_numbers[random_area]
#         print(f'''
# player_areas: {player_areas}
# random_area: {random_area}
# area_numbers: {area_numbers}
# target: {target}
#               ''')

        point=area_dict[target]
        value=map_dict[point]
        #print(value)
        if value==1:
            map_dict[point]=-1
        elif value==2:
            map_dict[point]=-2
        elif value==3:
            map_dict[point]=-3
        else:
            map_dict[point]=-4
        
        # Also check for loss:
        if value>1:
            ai_hit_target=True
            remove_ship_point(point,player)
            
        count_boats_remaining(player)
        
        ships_now=fleet["boats"]
        if ships_now<=0:
            #print("debug: Your fleet has been sunk, unfortunately!")
            #print("")
            return
        
        if value>1:
            print("You've been hit!")
            print("")

equal_line="==============================================================================="

def show_main_menu():
    print(equal_line)
    print('''
Welcome to Battleships!
-----------------------''')
    
    print(f'''
Current settings:

Map size: {map_dimensions[0]} x {map_dimensions[1]}
Ships: {ships[0]} small, {ships[1]} medium, {ships[2]} large
    ''')
    print(equal_line)
    show_menu_action()

def action_map_size():
    print(f'''
{equal_line}
          
Current map size: {map_dimensions[0]} x {map_dimensions[1]}
-----------------

Please type in the format: X Y (for example: 3 4)

Minimum map size: 3 x 3
Maximum map size: 10 x 10.''')
    size=input("Assign map size: ")
    values=size.split(" ")
    values_l=len(values)
    #print(values_l)
    if values_l<2 or values_l>2:
        print('''
Invalid format.''')
        #print("Please type two numbers in the format X Y (for example: 3 4).")
        action_map_size()
    else:
        x=values[0]
        y=values[1]
        if not x.isdigit() or not y.isdigit():
            print('''
Two numbers are required.''')
            action_map_size()
        else:
            x=int(x)
            y=int(y)
            if x<3 or x>10 or y<3 or y>10:
                print('''
Assigned size is not within the allowed dimensions.''')
                action_map_size()
            else:
                # At this point, there shouldn't be a problem?...
                map_dimensions[0]=x
                map_dimensions[1]=y
                print(f'''
New map size is {map_dimensions[0]} x {map_dimensions[1]}.
''')
                show_main_menu()

def action_boat_count():
    print(f'''
{equal_line}
    
Current ship count: {ships[0]} small, {ships[1]} medium, {ships[2]} large
-------------------

Please type in the format: X Y Z (for example: 1 0 0)

Ship sizes:

SS  MM  LL
SS  MM  LL
    MM  LL
        LL''')

# A ship cannot be longer than the map size.
        
    assigned_ships=input("Assign ships: ")
    
    values=assigned_ships.split(" ")
    values_l=len(values)
    #print(values_l)
    if values_l<3 or values_l>3:
        print('''
Invalid format.''')
        #print("Please type two numbers in the format X Y (for example: 3 4).")
        action_boat_count()
    else:
        x=values[0]
        y=values[1]
        z=values[2]
        if not x.isdigit() or not y.isdigit() or not z.isdigit():
            print('''
Three numbers are required.''')
            action_boat_count()
        else:
            x=int(x)
            y=int(y)
            z=int(z)
            total_ships=x+y+z
            if total_ships<=0:
                print('''
At least 1 ships needs to be assigned to the battle.''')
                action_boat_count()
            else:
                # check boat size vs map dimensions...
                map_x=map_dimensions[0]
                map_y=map_dimensions[1]
                map_highest=map_x
                if map_y>map_x:
                    map_highest=map_y
                else:
                    map_highest=map_x

                if z>0:
                    boat_highest=z
                elif y>0:
                    boat_highest=y
                else:
                    boat_highest=x
                
                if boat_highest>map_highest:
                    print('''
Assigned boats cannot be larger than the map.''')
                    action_boat_count() 
                else:
                    # At this point, there shouldn't be any issues:
                    ships[0]=x
                    ships[1]=y
                    ships[2]=z
                    show_main_menu()

def show_menu_action():
    action=input(f'''1. Change map size
2. Change ship count
3. Start game

Choose action: ''')

    if not action.isdigit():
        print("")
        print("Please type a number corresponding to a menu action.")
        show_menu_action()
    else:
        number=int(action)
        
        # so first ~ set map size:
        if number==1:
            action_map_size()

        if number==2:
            action_boat_count()

        if number==3:
            # start game!
            print("")
            print(f'''Game starting...

{equal_line}''')

            add_boats(ships[0],ships[1],ships[2],player)
            add_boats(ships[0],ships[1],ships[2],ai)
            
            count_boats_remaining(player)
            count_boats_remaining(ai)

            print(f'''
Your fleet. Ships remaining: {fleet["boats"]}''')

            print_map(player)
            create_attack_map(player,1)
        
        if number>3:
            print("")
            print("Please type a number corresponding to a menu action.")
            show_menu_action()

show_main_menu()
