#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pandas import DataFrame
from parse import *
from termcolor import colored
from colored import fg, bg, attr

color_orc = fg('orchid') + attr('bold')
color_yel = fg('light_goldenrod_2b') + attr('bold')
color_org = fg('dark_orange') + attr('bold')
color_gren = fg('chartreuse_3b') + attr('bold')
bold = attr('bold')
res = attr('reset')

''' This function is used to populate BARCODE, DESCRIPTION, POS-X, POS-Y, EXTERNALAISLEID in the CSV file. 
    It will iterate based on the information of the first var section'''
def bin_iteration():
    print('hello world')
    global total_length
    global uniq_counter
    print('')
    print('%s%sEnter Varied Coordinate Info: %s' % (fg('dark_orange'), attr('bold'), attr('reset'))) 

    #Set Initial and Final Coordinate for Aisle Section
    cont = 'place_holder'
    while cont != '':
        if x_y_static == 'y':
            y_int = float(input('What is y initial?  '))
            y_fin = float(input('What is y final?  '))
            y_static = int(input('How many iterations is y static?  '))
        else:
            y_int = float(input('What is x initial?  '))
            y_fin = float(input('What is x final?  '))   
            y_static = int(input('How many iterations is x static?  '))     

        y_fin *= 1000
        y_int *= 1000 
        print('')
        cont = input('Confirm Coordinates - Press enter. Else - Press any letter.  ')   
    
    #Varied Component Information
    if (uniq_section[uniq_counter] - 1) != var_counter: 
        unq_lst_len.append(str(0))
        p_i = int(v_initial[0])
        p_f = int(v_final[0])

        var_step_int = int(var_step[0])
        if p_f < p_i and int(var_step[0]) > 0: var_step_int *= -1
        if p_i < p_f and int(var_step[0]) < 0: var_step_int *= -1
        p_step = var_step_int; var_step[0] = var_step_int
 
        #Total length of numbers in the varied component for an aisle section
        var_length = int(abs((p_i - p_f)/p_step)) + 1  
    #Unique Component Information
    else:
        print('')
        print('%s%sEnter Unique Var Section 1 Info: %s' % (fg('orchid_2'), attr('bold'), attr('reset')))
        cont = 'place_holder'
        while cont != '':
            lst = input('Please input unique list with a space in between each item:  ')
            unique_it = int(input('How many iterations of unique list for aisle section?  '))
            print('')
            cont = input('Confirm Unique Section Info - Press enter. Else - Press any letter.  ') 
        lst = lst.split()
        var_length = (len(lst)) 
        unq_lst_len.append(str(len(lst)))
    
    p_static = int(var_static[0])

    # Normal Var Section 1 Bin Location Iteration
    if (uniq_section[uniq_counter] - 1) != var_counter: 
        total_length = var_length * p_static
        for i in range(1,(var_length + 1)): 
            for j in range(1,(p_static + 1)):
                barcode_tot = str(barcode_int) + str(p_i).zfill(fill) 
                BARCODE.append(str(barcode_tot))
                DESCRIPTION.append(aisle_description)
                EXTERNALAISLEID.append(ext_ID)
                if x_y_static == 'y':
                    POS_X.append(static_coord)
                else:
                    POS_Y.append(static_coord)       
            p_i += p_step
    
    #Unique Var Section 1 Bin Location Iteration
    else: 
        num = 1
        k = 0
        total_length = (var_length * p_static) * unique_it
        for i in range(total_length):    
            barcode_tot = str(barcode_int) + str(lst[k]).zfill(fill) 
            BARCODE.append(str(barcode_tot))
            num += 1
            if num > p_static:
                k += 1 
                num = 1
            if (k + 1) > len(lst):
                k = 0  
            DESCRIPTION.append(aisle_description)
            EXTERNALAISLEID.append(ext_ID)
            if x_y_static == 'y':
                POS_X.append(static_coord)
            else:
                POS_Y.append(static_coord)       
  
    #Varied X/Y Coordinate Iteration
    chuck_stops = (total_length/y_static) - 1
    #y_step is the distance between each bin location x,y coord in millimeters
    y_step = (y_fin - y_int)/(chuck_stops)
    y_counter = 1
    for i in range(total_length):
        if x_y_static == 'y':
            POS_Y.append(str(round(y_int)))
        else:
            POS_X.append(str(round(y_int)))
        y_counter += 1
        if y_counter > y_static: 
            y_int += y_step
            y_counter = 1  
    if ((uniq_section[uniq_counter] - 1) == var_counter and len(uniq_section) > 1): uniq_counter +=1       

'''This function is used to append each barcode in an aisle section with additional var components.'''
def var_iteration(): 
    global update_i
    zoo = update_i
    unq_lst_len.append(str(0))

    #Normal Varied Component Information
    p_i = int(v_initial[var_counter])
    p_f = int(v_final[var_counter])

    var_step_int = int(var_step[var_counter])
    if p_f < p_i and int(var_step[var_counter]) > 0: var_step_int *= -1
    if p_i < p_f and int(var_step[var_counter]) < 0: var_step_int *= -1
    p_step = var_step_int; var_step[var_counter] = var_step_int

    p_static = int(var_static[var_counter]) 
    
    p_value = p_i
    var = 1
    #Normal Varied Component Iteration - Appends each barcode in aisle section
    for i in range(total_length):
        BARCODE[zoo] += (str(p_value).zfill(fill))
        zoo += 1
        var += 1
        if var > p_static:
            p_value += p_step
            var = 1
        if p_value > p_f and p_f > p_i: p_value = p_i
        if p_value < p_f and p_f < p_i: p_value = p_i

'''This function is used to append each barcode in an aisle section with additional unique var components.'''
def unique_iteration():
    global update_i, uniq_counter
    zoo = update_i
    print('')
    print('%s%sEnter Info For Unique Var Section %s' % (fg('orchid_2'), attr('bold'), attr('reset')) + color_orc + str(var_counter + 1) + res)
    
    #Unique Component Information
    cont = 'place_holder'
    while cont != '':
        lst = input('Please input unique list with a space in between each item:  ')
        cont = input('Confirm Unique Section Info - Press enter. Else - Press any letter.  ')
    lst = lst.split()
    p_static = int(var_static[var_counter])  
    unq_lst_len.append(str(len(lst)))
    
    j = 0  
    var = 1  
    #Unique Component Iteration - Appends each barcode in aisle section
    for i in range(total_length):
        BARCODE[zoo] += (str(lst[j]))
        zoo += 1
        var += 1
        if var > p_static:
            j += 1 
            var = 1
        if (j + 1) > len(lst):
            j = 0  
    if len(uniq_section) > 1: uniq_counter += 1

'''This function is used to append each barcode in an aisle section with a grid component.'''
def grid_iteration():
    global update_i, grid_index
    zoo = update_i
    #Normal Grid Component Information
    if (uniq_section[uniq_counter] - 1) != var_counter:
        unq_lst_len.append(str(0))
        grid_i = int(v_initial[var_counter])
        p_step = (int(var_step[var_counter]))
        v_initial[var_counter] = grid_i + p_step

        #Normal Grid Component Iteration - Appends each barcode in aisle section
        for i in range(total_length):
            BARCODE[zoo] += (str(grid_i).zfill(fill))
            zoo += 1
    #Unique Grid Component Information
    else:
        print('hello world')
        # ##add list here maybe
        # unq_lst_len.append(str(len(lst)))
        # grid_i = lst[grid_index]
        # grid_index += 1

        # #Unique Grid Component Iteration - Appends each barcode in aisle section
        # for i in range(total_length):
        #     BARCODE[zoo] += (str(grid_i).zfill(fill))
        #     zoo += 1

'''Input External aisle ID, aisle description, static coordinate, # of aisle sections'''
def aisle_info():
    print('')
    print('%s%sEnter Aisle Info: %s' % (fg('light_goldenrod_2b'), attr('bold'), attr('reset')))
    global aisle, ext_ID, aisle_sections, aisle_description, static_coord, staticcoord_lst
    global extID_lst, total_aisles, grid_section
    cont = 'place_holder'
    #Aisle Information
    while cont != '':
        if grid == 'n':
            ext_ID = input('What is the external aisle ID?  ')
            extID_lst.append(ext_ID)
            aisle_sections = int(input('How many aisle sections for a single virtual aisle?  '))
            static_coord = str(round(float(input('What is the static coordinate?  ')) * 1000))
            aisle_description = 'aisle ' + ext_ID
        else:
            aisle_sections = 1
            extID_lst = '218 219 220'#input('Please input ext ID list with a space in between each item:  ')
            extID_lst = extID_lst.split()
            staticcoord_lst = '2 5 10'#input('Please input ext ID list with a space in between each item:  ')
            staticcoord_lst = staticcoord_lst.split()
            total_aisles = 3#int(input('How many aisles to map bin locations?  '))
            ###add a way to add a second grid section####
            grid_section = 0#int(input('What var section is the grid section?  ')) - 1
        print('')
        cont = input(color_gren + 'Confirm Aisle Information - Press enter. Else - Press any letter.  ' + res)

'''Input var step and var static for each var section'''
def var_step_var_static():
    cont = 'place_holder'
    global var_step, var_static
    print('')
    print('%s%sEnter Var Step and Static Info: %s' % (fg('light_goldenrod_2b'), attr('bold'), attr('reset'))) 
    #Var Step and Static information for each Var Section
    while cont != '':
        var_step = []; var_static = []
        for i in range(var_section):
            var_step.append(input('Var Section ' + str(i + 1) + ': What is the var step?  '))
        print('')
        for i in range(var_section):
            var_static.append(input('Var Section ' + str(i + 1) + ': How many iterations is var static?  '))
        print('')
        cont = input(color_gren + 'Confirm Var Step and Var Static - Press enter. Else - Press any letter.  ' + res)

'''Input var initial and var final for each var section.  The z-fill for the var section is determined
    by the number of characters in each var final'''
def var_int_var_fin_z_fill():
    cont = 'place_holder'
    global v_initial, v_final, z_fill
    print('')
    print('%s%sEnter Var Initial and Final Info: %s' % (fg('light_goldenrod_2b'), attr('bold'), attr('reset')))
    a = string_structure.replace(':.1',''); a = a.replace(':.2',''); a = a.replace(':.3',''); a = a.replace(':.4',''); a = a.replace(':.5','')
    #Var Initial and Final information for each Var Section
    while cont != '':
        j = 0
        v_initial = []; v_final = []; z_fill = []
        for i in range(var_section):
            v_initial.append(input('Var Section ' + str(i + 1) + ': What is the initial var?  ' ))
        j = 0
        print('')
        for i in range(var_section):
            v_final.append(input('Var Section ' + str(i + 1) + ': What is the final var?  ' ))
        #Z-fill for Var Sections determined by length of var final
        for i in range(len(v_final)):
            z_fill.append(len(v_final[i]))

        #Print Initial and Final Barcode
        temp_i = v_initial; temp_f = v_final
        var_lst_length = 5 - len(v_initial)
        for i in range(var_lst_length):
            temp_i.append('0')
            temp_f.append('0')
        var1, var2, var3, var4, var5 = temp_i
        var6, var7, var8, var9, var10 = temp_f
        print('')
        print(bold + 'Z-fill for Var Sections: ' + str(z_fill))
        print('Initial Bin Location: ' + a.format(var1, var2, var3, var4, var5))
        print('Final Bin Location: ' + a.format(var6, var7, var8, var9, var10) + res)
        print('')
        cont = input(color_gren + 'Confirm Var Initial and Var Final - Press enter. Else - Press any letter.  ' + res)

'''Input x coordinate, z coordinate, and unique component information.'''
def x_z_uniq_info():
    global x_y_static, z_change, z_value, unique, uniq_section2, uniq_section
    print('')
    print('%s%sEnter Coordinate/Unique Info: %s' % (fg('light_goldenrod_2b'), attr('bold'), attr('reset')))
    cont = 'place_holder'
    #Coordinate Info and Unique Component Info
    while cont != '':
        uniq_section = [0]
        x_y_static = input('Is the X coordinate static (y/n)?  ')
        z_change = input('Is the Z coordinate static (y/n)?  ')
        if z_change == 'n':
            z_coord_questions()
        else:
            z_value = 1
        unique = input('Is there an unique component (y/n)?  ')
        if unique == 'y': 
            print('')
            print('%s%sEnter Unique Section Info: %s' % (fg('light_goldenrod_2b'), attr('bold'), attr('reset')))
            uniq_section = '1 2'#input('Please input unique var section list with a space in between each item:  ')
            uniq_section = uniq_section.split()
            # uniq_section[0] = (int(input('What var section does unique component correspond to?  ')))
            # uniq_section2 = input('No second unique component? Press Enter. Else enter var section number.  ')
            # if uniq_section2 != '': uniq_section.append(int(uniq_section2))
        print('')
        cont = input(color_gren + 'Confirm Inputs - Press enter. Else - Press any letter.  ' + res)

'''Input additional information regarding z-coordinate if z is not static'''
def z_coord_questions():
    print('')
    print('%s%sEnter Z Coordinate Info: %s' % (fg('light_goldenrod_2b'), attr('bold'), attr('reset')))
    #Z Corresponds to Var Section - Or Input Manually
    global res_1, res_2, z_int, z_fin, z_step, z_static, z_value
    cont = 'place_holder'
    while cont != '':
        res_1 = input('Does Z coord correspond to a uniq section (c), var section (v), or input manually (m)?  ')
        
        if res_1 == 'c' or res_1 == 'v':
            #res_2 corresponds to var_counter
            res_2 = int(input('What var section does z correspond to?  ')) - 1 
        else:
            z_int = int(input('What is the first z value?  '))
            z_fin = int(input('What is the final z value?  '))
            z_step = int(input('What is the z step?  ')) 
            z_static = int(input('How many iterations is z static ?  '))
            z_value = z_int  
            if z_fin < z_int and z_step > 0: z_step *= -1
            if z_int < z_fin and z_step < 0: z_step *= -1  
        print('')
        cont = input(color_gren + 'Confirm Z Coordinate Info - Press enter. Else - Press any letter.  ' + res)
        print('')

'''The function will iterate the z-coordinate for all barcodes in an aisle section and populate the data field
POS-Z in the CSV file'''
def z_coordinate():
    global total_length
    print('')
    if z_change == 'y':
        z_value = 1
    #Z Corresponds to Var Section - Or Input Manually
    else:
        #Z Corresponds to a Unique Var Section
        if res_1 == 'c':
            z_int = 1
            z_step = 1
            z_value = z_int 
            #res_2 corresponds to var_counter
            z_static = int(var_static[res_2]) 

            if len(unq_lst_len) == 1:
                z_fin = int(unq_lst_len[0])
            else:
                z_fin = int(unq_lst_len[res_2])
        #Z is Identical to a Normal Var Section
        if res_1 == 'v':
            z_int = int(v_initial[res_2])
            z_fin = int(v_final[res_2])
            z_step = int(var_step[res_2])
            z_static = int(var_static[res_2])
            z_value = z_int  
 
    #Iterate for Z = 1
    if z_change == 'y':
        for i in range(total_length):
            POS_Z.append(str(z_value))
    #Iterate for Varied Z Coordinate
    else:
        hi = 1
        var = 1
        for i in range(total_length):
            POS_Z.append(str(z_value))
            hi += 1
            var += 1
            if var > z_static:
                z_value += z_step
                var = 1
            if z_value > z_fin and z_fin > z_int: z_value = z_int
            if z_value < z_fin and z_fin < z_int: z_value = z_int 

'''This function is used to parse the bin structure to identify the static components'''          
def parse_info():
    global statics
    static_phrase = ''
    end = len(string_structure)
    for i in range(end):
        if string_structure[i] != '{' and string_structure[i] != '}':
            static_phrase += string_structure[i]
        if string_structure[i] == '{' or string_structure[i] == '}' or (i == (end - 1)):
            if ':' and 'd' in static_phrase:
                static_phrase = ''
            elif ':' and '.' in static_phrase: 
                static_phrase = ''
            else:
                statics.append(str(static_phrase))
                static_phrase = ''   
    statics = list(filter(None, statics))   

'''This function is used to parse the bin structure to identify the order of static and varied components'''
def section_type_parse():
    global var_section, barcode_components
    a = string_structure.replace(':.1',''); a = a.replace(':.2',''); a = a.replace(':.3',''); a = a.replace(':.4',''); a = a.replace(':.5','')
    start = 0
    end = len(a)
    char = '{'
    char2 = '}'
    while(start < end):
        ind = a.find(char,start,end)
        if(ind > -1):
            if(start != ind):
                section_type.append(0)
            i = 1
            while(ind + i < end and (a[ind + i] == char2)):
                i = i + 1
            section_type.append(1)
            start = ind + i
        else:
            if(start != end):
                section_type.append(0)
            break 
    var_section = section_type.count(1)
    barcode_components = len(section_type)

'''This function is used to export and update the bin location CSV after each aisle section'''    
def export_csv():
    global new_filename
    if update_i != 0:
        old_filename = new_filename
    if len(extID_lst) == 1:
        new_filename = 'A' + str(ext_ID) + '.csv'
    else:
        new_filename = 'A' + str(extID_lst[0]) + '_to_' + 'A' + str(ext_ID) + '.csv'
    if update_i != 0:
        os.remove(old_filename)
    d = {'BARCODE': BARCODE,
        'DESCRIPTION': DESCRIPTION,
        'POS-X': POS_X,
        'POS-Y': POS_Y,
        'POS-Z': POS_Z,
        'EXTERNALAISLEID': EXTERNALAISLEID}
    df = DataFrame(d, columns = ['BARCODE', 'DESCRIPTION', 'POS-X', 'POS-Y','POS-Z','EXTERNALAISLEID'])
    df.to_csv (new_filename, index = None, header = True)

###########################################################################################################################
###########################################################################################################################

#Lists for final csv 
BARCODE = []; DESCRIPTION = []; POS_X = []; POS_Y = []; POS_Z = []; EXTERNALAISLEID = []
cont = ''
inputs = ''
update_i = 0
extID_lst = []
print('')
grid = input(bold + 'Are the aisles in a grid pattern?(y/n)  ' + res)

if grid == 'n':
    while cont == '':
        #Enter bin location initial structure, aisle #, static coord, external ID
        print(''); print('%s%sGenerating Bin Locations . . . %s' % (fg('steel_blue_1a'), attr('bold'), attr('reset')))
        section_type = []; statics = []
        aisle_info(); print('')
        string_structure = input('%s%sDefine the Bin Location Structure:  %s' % (fg('steel_blue_1a'), attr('bold'), attr('reset')))
        section_type_parse(); parse_info()
        #print(section_type); print(statics)

        #Enter Varied Component info, additional coord info, unique section info, z coord info for first aisle section
        if update_i == 0:
            #enter varstep and varstatic; enter x,z,unique component info 
            var_static = []; var_step = []; uniq_section = [0]
            x_z_uniq_info()
            var_step_var_static()    

        #Iterate for each aisle section in an aisle
        for k in range(1, aisle_sections + 1): 
            print('')
            print(color_gren +'External Aisle ID: ' + str(ext_ID) + '; Aisle Section: ' + (str(k)) + res)
            z_fill = []; v_initial = []; v_final = []; unq_lst_len = [] 
            var_counter = 0; static_counter = 0; uniq_counter = 0; barcode_int = ''
            
            while inputs != '':
                print('')
                #change bin location structure
                if inputs == 's':
                    section_type = []; statics = []
                    string_structure = input('%s%sDefine the Bin Location Structure:  %s' % (fg('steel_blue_1a'), attr('bold'), attr('reset')))
                    section_type_parse(); parse_info()
                    #uniq_section = [0]
                    #print(section_type); print(statics)
                #change varied component info (var step and var static)
                if inputs == 'v':
                    var_static = []; var_step = []
                    var_step_var_static() 
                #change coordinate and unique section info
                if inputs == 'c': #create a function 
                    uniq_section = [0]
                    x_z_uniq_info()  
                if inputs == 'sc':
                    static_coord = str(round(float(input('What is the static coordinate?  ')) * 1000))
                print('')
                inputs = input('Any additional changes? No - press enter. Else - bin structure (s), var step/static (v), x,z,uniq info (c), static coord (sc)  ')   
            
            var_int_var_fin_z_fill() 
            #Iterate for all bin locations in one aisle section
            for i in range(1, (barcode_components + 1)):
                #Static Section - Bin Location Iteration
                if section_type[i - 1] == 0: 
                    if static_counter == 0 and var_counter == 0:
                        barcode_int = statics[0]
                        static_counter += 1  
                    else:
                        baz = update_i
                        for i in range(total_length):
                            BARCODE[baz] += statics[static_counter]
                            baz += 1
                        static_counter += 1
                #Varied Section - Bin Location Iteration        
                else: 
                    #Iterate for all bin locations
                    if var_counter == 0:
                        fill = z_fill[var_counter]
                        bin_iteration()
                        var_counter += 1
                    else: 
                        #Append bin location with normal varied section
                        if (uniq_section[uniq_counter] - 1) != var_counter:
                            fill = z_fill[var_counter]
                            var_iteration()
                            var_counter += 1
                        #Append bin location with unique varied section
                        else:
                            fill = z_fill[var_counter]
                            unique_iteration()
                            var_counter += 1
            z_coordinate() 
            d = {'BARCODE': BARCODE,'DESCRIPTION': DESCRIPTION,'POS-X': POS_X,'POS-Y': POS_Y,'POS-Z': POS_Z,'EXTERNALAISLEID': EXTERNALAISLEID}
            df = DataFrame(d, columns= ['BARCODE', 'DESCRIPTION', 'POS-X', 'POS-Y','POS-Z','EXTERNALAISLEID'])
            print (df)  
            export_csv()
            update_i += total_length
            print('')
            cont = input('Do you wish to continue to next aisle? Press enter. Else - any letter  ')
            if cont != '':
                break
            print('')
            inputs = input('Will inputs change? (bin structure (s), var step/static (v), x,z,uniq info (c), static coord (sc) Else press enter.  ')      

    export_csv()
    print('')
    print('%s%sBin Locations Exported: %s' % (fg('steel_blue_1a'), attr('bold'), attr('reset'))) 

    d = {'BARCODE': BARCODE,
        'DESCRIPTION': DESCRIPTION,
        'POS-X': POS_X,
        'POS-Y': POS_Y,
        'POS-Z': POS_Z,
        'EXTERNALAISLEID': EXTERNALAISLEID} 
    df = DataFrame(d, columns= ['BARCODE', 'DESCRIPTION', 'POS-X', 'POS-Y','POS-Z','EXTERNALAISLEID'])
    print (df) 
else:
    print('yay grids')
