# Copyright   : @TacticsBadger, TacticsNotAntics: https://tacticsnotantics.org
# Modified by : HitBrann, GitBrann: https://github.com/HitBrann
# Version 1.0 : November 17, 2021
# Last Updated: January 08, 2022
'''
Brief: Monte Carlo simulations for predicting match outcomes.
Needs user input: keyboard or csv. 
'''
import sys
import time
import pandas as pd
import numpy as np
from prettytable import PrettyTable
from mysql.connector import Error,connect

#Importar librerias para manejo de archivos
import pandas as pd

def Montecarlo(host_db:str,user_db:str,password_db:str,port_db:int,local_team:str=None, away_team:str=None, n:int=None,)->int: 
    """
    This function runs the Monte Carlo simulation for match outcomes.

    Parameters
    ----------
    local_team: str 
        The local team
    away_team: str
        The away team
    n: int
        Number of simulations
    host_db : str
        Host of the database
    user_db : str
        User of the database
    password_db : str
        Password of the database
    port_db : int
        Port of the database

    Returns
    -------
    int
        This function returns 0 if is more probable that the home team wins, 1 if is more probable that the away team wins and 2 if is more probable that the match ends in a draw.

    Examples
    --------
    >>> Montecarlo("América", "Pumas", 100, "127.0.0.1", "admin", "justapassword", 3306)
    Bienvenido al simulador de partidos
    Seleccione un equipo local a comparar
    .
    .
    .
    Recomendación: Apostar por el equipo local
    """
    print("***************** Tactics Not Antics ******************")
    print("*****          Monte Carlo Match Simulator        *****")
    print("*****        Version 1.0: November 17, 2021       *****")
    print("*****        Last Update: January  08, 2021       *****")
    print("*******************************************************")
    print("******************* Mod by: GitBrann ******************")
    #Connect to the database
    try: 
        with connect(
            host=host_db,
            user=user_db,
            password=password_db,
            autocommit = True,
            port = port_db
        ) as conn:
            if conn.is_connected():
                print("Conectado a la base de datos" 
       )
            #We get the teams and their xG from the database
            cursor = conn.cursor()
            cursor.execute("USE LIGA_MX")
            cursor.execute("SELECT equipo, xG_L, xG_V FROM xG")
            #We create a dataframe with the data
            df = pd.DataFrame(cursor.fetchall())
            df.columns = cursor.column_names
            #We create a list with the teams
            teams = df['equipo'].tolist()
            #We create a list with the xG of the teams
            xG_L = df['xG_L'].tolist()
            #We create a list with the xG of the teams
            xG_V = df['xG_V'].tolist()
            #-----For update purposes
            #we get the max goals scored by a team in home position from the database
            #cursor.execute("SELECT MAX(goles_local) FROM PARTIDOS")
            #max_goals_home = cursor.fetchone()
            #we get the max goals scored by a team in away position from the database
            #cursor.execute("SELECT MAX(goles_visitante) FROM PARTIDOS")
            #max_goals_away = cursor.fetchone()
    except Error as e:
        print("Error while connecting to MySQL", e)
    if n == None:
        num_simulations = 20000
    else:
        num_simulations = n
    try:
        print ("Bienvenido al simulador de partidos")
        print("Seleccione un equipo local a comparar")
        print("1. América")
        print("2. Atlas")
        print("3. Club Atlético de San Luis")
        print("4. Cruz Azul")
        print("5. FC Juárez")
        print("6. Guadalajara")
        print("7. León")
        print("8. Mazatlán FC")
        print("9. Monterrey")
        print("10. Necaxa")
        print("11. Pachuca")
        print("12. Puebla")
        print("13. Pumas")
        print("14. Querétaro")
        print("15. Santos Laguna")
        print("16. Tigres")
        print("17. Tijuana")
        print("18. Toluca")
        print("0. Salir")
        intentos_local=0
        while True:
            try:
                if local_team == None:
                    input_home_team = input("* Selecciona un equipo local(Número): ")
                else:
                    input_home_team = str(local_team)
                #We make every input
                if input_home_team == "1":
                    input_home_team = "América"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "2":
                    input_home_team = "Atlas"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "3":
                    input_home_team = "Club Atlético de San Luis"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "4":
                    input_home_team = "Cruz Azul"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "5":
                    input_home_team = "FC Juárez"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "6":
                    input_home_team = "Guadalajara"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "7":
                    input_home_team = "León"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "8":
                    input_home_team = "Mazatlán FC"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "9":
                    input_home_team = "Monterrey"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "10":
                    input_home_team = "Necaxa"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "11":
                    input_home_team = "Pachuca"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "12":
                    input_home_team = "Puebla"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "13":
                    input_home_team = "Pumas"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "14":
                    input_home_team = "Querétaro"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "15":
                    input_home_team = "Santos Laguna"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "16":
                    input_home_team = "Tigres"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "17":
                    input_home_team = "Tijuana"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif input_home_team == "18":
                    input_home_team = "Toluca"
                    #We get the home team position in the list of teams
                    local_pos = teams.index(input_home_team)
                    #We get the home team xG
                    input_home_team_xg = xG_L[local_pos]
                    break
                elif int(input_home_team) == 0:
                    print("Saliendo del programa...")
                    sys.exit()
                else:
                    print("El valor ingresado no es válido")
                    intentos_local = intentos_local + 1
                if intentos_local == 2:
                    print("Algo salió mal, revisa que la normalización de los datos coincida con la requerida por el programa")
                    sys.exit()
            except ValueError:
                print("El valor ingresado no es válido")
                intentos_local = intentos_local + 1
            except NameError:
                print("El valor ingresado no es válido")
                intentos_local = intentos_local + 1
        #We print the team selected and its xG
        print("Equipo local: ", input_home_team, " xG: ", input_home_team_xg)
    except UnboundLocalError:
        print("Posible error en base de datos detectado")
        print("Verifica que hayas actualizado la base de datos antes de ejecutar las simulaciones")
        print("Tambien puedes verificar que tu base de datos funcione correctamente")
        print("Asegurate de que los datos en el archivo ./dev/databases.json sean correctos y correspondan a tu base de datos.")
        print("Verifica los permisos de la cuenta accesada en tu base de datos")
        sys.exit()
    print ("Bienvenido al simulador de partidos")
    print("Seleccione un equipo visitante a comparar")
    print("1. América")
    print("2. Atlas")
    print("3. Club Atlético de San Luis")
    print("4. Cruz Azul")
    print("5. FC Juárez")
    print("6. Guadalajara")
    print("7. León")
    print("8. Mazatlán FC")
    print("9. Monterrey")
    print("10. Necaxa")
    print("11. Pachuca")
    print("12. Puebla")
    print("13. Pumas")
    print("14. Querétaro")
    print("15. Santos Laguna")
    print("16. Tigres")
    print("17. Tijuana")
    print("18. Toluca")
    print("0. Salir")
    intentos_visitante = 0
    while True:
        try:
            if away_team == None:
                input_away_team = input("* Selecciona un equipo visitante(Número): ")
            else:
                input_away_team = str(away_team)
            #We make every input
            if input_away_team == "1":
                input_away_team = "América"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "2":
                input_away_team = "Atlas"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "3":
                input_away_team = "Club Atlético de San Luis"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "4":
                input_away_team = "Cruz Azul"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "5":
                input_away_team = "FC Juárez"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "6":
                input_away_team = "Guadalajara"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "7":
                input_away_team = "León"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "8":
                input_away_team = "Mazatlán FC"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "9":
                input_away_team = "Monterrey"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "10":
                input_away_team = "Necaxa"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "11":
                input_away_team = "Pachuca"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "12":
                input_away_team = "Puebla"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "13":
                input_away_team = "Pumas"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "14":
                input_away_team = "Querétaro"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "15":
                input_away_team = "Santos Laguna"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "16":
                input_away_team = "Tigres"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "17":
                input_away_team = "Tijuana"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif input_away_team == "18":
                input_away_team = "Toluca"
                #We get the away team position in the list of teams
                local_pos = teams.index(input_away_team)
                #We get the away team xG
                input_away_team_xg = xG_V[local_pos]
                break
            elif int(input_away_team) == 0:
                print("Saliendo del programa...")
                sys.exit()
            else:
                print("El valor ingresado no es válido")
                intentos_visitante += 1
            if intentos_visitante >= 2:
                print("Algo salió mal, revisa que la normalización en la base de datos sea la requerida por el programa.")
        except ValueError:
            print("El valor ingresado no es válido")
            intentos_visitante += 1
        except NameError:
            print("El valor ingresado no es válido")
            intentos_visitante += 1
    #We print the team selected and its xG
    print("Equipo visitante: ", input_away_team, " xG: ", input_away_team_xg)
    #convert the input to the correct data types
    input_home_team = str(input_home_team)
    input_home_team_xg = float(input_home_team_xg)
    input_away_team = str(input_away_team)
    input_away_team_xg = float(input_away_team_xg)
    if input_home_team == input_away_team:
        print("Error: Los equipos no pueden ser el mismo.")
        sys.exit()
    #print the simulation table and run simulations
    print ("**************************")
    print ("*                        *")
    print ("* GENERANDO SIMULACIONES *")
    print ("*                        *")
    print ("**************************")
    count_home_wins = 0
    count_home_loss = 0
    count_away_wins = 0
    count_away_loss = 0
    count_draws = 0
    score_mat = []
    tot_sim_time = 0
    sim_table = PrettyTable(["SIMULACIÓN #", "TIEMPO SIMULACIÓN (s)", input_home_team, input_away_team, "GANA LOCAL", "GANA VISITANTE", "EMPATE", "MARGEN DE PUNTAJE"])
    for i in range(num_simulations):
        #get simulation start time
        start_time = time.time()
        #run the sim - generate a random Poisson distribution
        target_home_goals_scored = np.random.poisson(input_home_team_xg)
        target_away_goals_scored = np.random.poisson(input_away_team_xg)
        home_win = 0
        away_win = 0
        draw = 0
        margin = 0
        # if more goals for home team => home team wins
        if target_home_goals_scored > target_away_goals_scored:
            count_home_wins += 1
            count_away_loss += 1
            home_win = 1
            margin = target_home_goals_scored - target_away_goals_scored
        # if more goals for away team => away team wins
        elif target_home_goals_scored < target_away_goals_scored:
            count_away_wins += 1
            count_home_loss += 1
            away_win = 1
            margin = target_away_goals_scored - target_home_goals_scored
        elif target_home_goals_scored == target_away_goals_scored:
            draw = 1
            count_draws += 1
            margin = target_away_goals_scored - target_home_goals_scored
        # add score to score matrix
        score_mat.append((target_home_goals_scored, target_away_goals_scored))
        #get end time
        end_time = time.time()
        #add the time to the total simulation time
        tot_sim_time += round((end_time - start_time),5)
        #add the info to the simulation table
        sim_table.add_row([i+1, round((end_time - start_time),5), target_home_goals_scored, target_away_goals_scored, home_win, away_win, draw, margin])
    print(sim_table)
    # calculate probabilities to win/lose/draw
    home_win_probability = round((count_home_wins/num_simulations * 100),2)
    away_win_probability = round((count_away_wins/num_simulations * 100),2)
    draw_probability = round((count_draws/num_simulations * 100),2)
    # print the simulation statistics
    print ("***************************")
    print ("*                         *")
    print ("* ESTADISTICAS SIMULACIÓN *")
    print ("*                         *")
    print ("***************************")
    sim_table_stats = PrettyTable(["Total # of sims", "Total time (s) for sims", "HOME WINS", "AWAY WINS", "DRAWS"])
    sim_table_stats.add_row([num_simulations, round(tot_sim_time,3), count_home_wins, count_away_wins, count_draws])
    sim_table_stats.add_row(["-", "-", str(home_win_probability)+"%", str(away_win_probability)+"%", str(draw_probability)+"%"])
    print(sim_table_stats)
    # get the score matrix
    total_scores = len(score_mat)
    max_score = 7
    assemble_scores = [[0 for x in range(max_score)] for y in range(max_score)]
    for i in range(total_scores):
        if score_mat[i][0] == 0 and score_mat[i][1] == 0:
            assemble_scores[0][0] += 1
        elif score_mat[i][0] == 0 and score_mat[i][1] == 1:
            assemble_scores[0][1] += 1
        elif score_mat[i][0] == 0 and score_mat[i][1] == 2:
            assemble_scores[0][2] += 1     
        elif score_mat[i][0] == 0 and score_mat[i][1] == 3:
            assemble_scores[0][3] += 1     
        elif score_mat[i][0] == 0 and score_mat[i][1] == 4:
            assemble_scores[0][4] += 1    
        elif score_mat[i][0] == 0 and score_mat[i][1] == 5:
            assemble_scores[0][5] += 1
        elif score_mat[i][0] == 0 and score_mat[i][1] == 6:
            assemble_scores[0][6] += 1
        elif score_mat[i][0] == 1 and score_mat[i][1] == 0:
            assemble_scores[1][0] += 1
        elif score_mat[i][0] == 1 and score_mat[i][1] == 1:
            assemble_scores[1][1] += 1     
        elif score_mat[i][0] == 1 and score_mat[i][1] == 2:
            assemble_scores[1][2] += 1     
        elif score_mat[i][0] == 1 and score_mat[i][1] == 3:
            assemble_scores[1][3] += 1     
        elif score_mat[i][0] == 1 and score_mat[i][1] == 4:
            assemble_scores[1][4] += 1
        elif score_mat[i][0] == 1 and score_mat[i][1] == 5:
            assemble_scores[1][5] += 1
        elif score_mat[i][0] == 1 and score_mat[i][1] == 6:
            assemble_scores[1][6] += 1
        elif score_mat[i][0] == 2 and score_mat[i][1] == 0:
            assemble_scores[2][0] += 1
        elif score_mat[i][0] == 2 and score_mat[i][1] == 1:
            assemble_scores[2][1] += 1     
        elif score_mat[i][0] == 2 and score_mat[i][1] == 2:
            assemble_scores[2][2] += 1     
        elif score_mat[i][0] == 2 and score_mat[i][1] == 3:
            assemble_scores[2][3] += 1     
        elif score_mat[i][0] == 2 and score_mat[i][1] == 4:
            assemble_scores[2][4] += 1
        elif score_mat[i][0] == 2 and score_mat[i][1] == 5:
            assemble_scores[2][5] += 1
        elif score_mat[i][0] == 2 and score_mat[i][1] == 6:
            assemble_scores[2][6] += 1
        elif score_mat[i][0] == 3 and score_mat[i][1] == 0:
            assemble_scores[3][0] += 1
        elif score_mat[i][0] == 3 and score_mat[i][1] == 1:
            assemble_scores[3][1] += 1     
        elif score_mat[i][0] == 3 and score_mat[i][1] == 2:
            assemble_scores[3][2] += 1     
        elif score_mat[i][0] == 3 and score_mat[i][1] == 3:
            assemble_scores[3][3] += 1     
        elif score_mat[i][0] == 3 and score_mat[i][1] == 4:
            assemble_scores[3][4] += 1            
        elif score_mat[i][0] == 3 and score_mat[i][1] == 5:
            assemble_scores[3][5] += 1
        elif score_mat[i][0] == 3 and score_mat[i][1] == 6:
            assemble_scores[3][6] += 1
        elif score_mat[i][0] == 4 and score_mat[i][1] == 0:
            assemble_scores[4][0] += 1
        elif score_mat[i][0] == 4 and score_mat[i][1] == 1:
            assemble_scores[4][1] += 1     
        elif score_mat[i][0] == 4 and score_mat[i][1] == 2:
            assemble_scores[4][2] += 1     
        elif score_mat[i][0] == 4 and score_mat[i][1] == 3:
            assemble_scores[4][3] += 1     
        elif score_mat[i][0] == 4 and score_mat[i][1] == 4:
            assemble_scores[4][4] += 1   
        elif score_mat[i][0] == 4 and score_mat[i][1] == 5:
            assemble_scores[4][5] += 1
        elif score_mat[i][0] == 4 and score_mat[i][1] == 6:
            assemble_scores[4][6] += 1
        elif score_mat[i][0] == 5 and score_mat[i][1] == 0:
            assemble_scores[5][0] += 1
        elif score_mat[i][0] == 5 and score_mat[i][1] == 1:
            assemble_scores[5][1] += 1
        elif score_mat[i][0] == 5 and score_mat[i][1] == 2:
            assemble_scores[5][2] += 1
        elif score_mat[i][0] == 5 and score_mat[i][1] == 3:
            assemble_scores[5][3] += 1
        elif score_mat[i][0] == 5 and score_mat[i][1] == 4:
            assemble_scores[5][4] += 1
        elif score_mat[i][0] == 5 and score_mat[i][1] == 5:
            assemble_scores[5][5] += 1
        elif score_mat[i][0] == 5 and score_mat[i][1] == 6:
            assemble_scores[5][6] += 1
        elif score_mat[i][0] == 6 and score_mat[i][1] == 0:
            assemble_scores[6][0] += 1
        elif score_mat[i][0] == 6 and score_mat[i][1] == 1:
            assemble_scores[6][1] += 1
        elif score_mat[i][0] == 6 and score_mat[i][1] == 2:
            assemble_scores[6][2] += 1
        elif score_mat[i][0] == 6 and score_mat[i][1] == 3:
            assemble_scores[6][3] += 1
        elif score_mat[i][0] == 6 and score_mat[i][1] == 4:
            assemble_scores[6][4] += 1
        elif score_mat[i][0] == 6 and score_mat[i][1] == 5:
            assemble_scores[6][5] += 1
        elif score_mat[i][0] == 6 and score_mat[i][1] == 6:
            assemble_scores[6][6] += 1
    #calculate percentages and print the score matrix
    print ("*******************************************")        
    print ("*                                         *")       
    print ("*  MATRIZ DE PUNTUACIÓN (% PROBABILIDAD)  *")
    print ("*                                         *")
    print ("*******************************************")
    score_matrix = PrettyTable([" ", 0, 1, 2, 3, 4, 5, 6])
    score_matrix.add_row([0,round(assemble_scores[0][0]/num_simulations*100,2),round(assemble_scores[0][1]/num_simulations*100,2),round(assemble_scores[0][2]/num_simulations*100,2),round(assemble_scores[0][3]/num_simulations*100,2),round(assemble_scores[0][4]/num_simulations*100,2),round(assemble_scores[0][5]/num_simulations*100,2),round(assemble_scores[0][6]/num_simulations*100,2)])
    score_matrix.add_row([1,round(assemble_scores[1][0]/num_simulations*100,2),round(assemble_scores[1][1]/num_simulations*100,2),round(assemble_scores[1][2]/num_simulations*100,2),round(assemble_scores[1][3]/num_simulations*100,2),round(assemble_scores[1][4]/num_simulations*100,2),round(assemble_scores[1][5]/num_simulations*100,2),round(assemble_scores[1][6]/num_simulations*100,2)])
    score_matrix.add_row([2,round(assemble_scores[2][0]/num_simulations*100,2),round(assemble_scores[2][1]/num_simulations*100,2),round(assemble_scores[2][2]/num_simulations*100,2),round(assemble_scores[2][3]/num_simulations*100,2),round(assemble_scores[2][4]/num_simulations*100,2),round(assemble_scores[2][5]/num_simulations*100,2),round(assemble_scores[2][6]/num_simulations*100,2)])
    score_matrix.add_row([3,round(assemble_scores[3][0]/num_simulations*100,2),round(assemble_scores[3][1]/num_simulations*100,2),round(assemble_scores[3][2]/num_simulations*100,2),round(assemble_scores[3][3]/num_simulations*100,2),round(assemble_scores[3][4]/num_simulations*100,2),round(assemble_scores[3][5]/num_simulations*100,2),round(assemble_scores[3][6]/num_simulations*100,2)])
    score_matrix.add_row([4,round(assemble_scores[4][0]/num_simulations*100,2),round(assemble_scores[4][1]/num_simulations*100,2),round(assemble_scores[4][2]/num_simulations*100,2),round(assemble_scores[4][3]/num_simulations*100,2),round(assemble_scores[4][4]/num_simulations*100,2),round(assemble_scores[4][5]/num_simulations*100,2),round(assemble_scores[4][6]/num_simulations*100,2)])
    score_matrix.add_row([5,round(assemble_scores[5][0]/num_simulations*100,2),round(assemble_scores[5][1]/num_simulations*100,2),round(assemble_scores[5][2]/num_simulations*100,2),round(assemble_scores[5][3]/num_simulations*100,2),round(assemble_scores[5][4]/num_simulations*100,2),round(assemble_scores[5][5]/num_simulations*100,2),round(assemble_scores[5][6]/num_simulations*100,2)])
    score_matrix.add_row([6,round(assemble_scores[6][0]/num_simulations*100,2),round(assemble_scores[6][1]/num_simulations*100,2),round(assemble_scores[6][2]/num_simulations*100,2),round(assemble_scores[6][3]/num_simulations*100,2),round(assemble_scores[6][4]/num_simulations*100,2),round(assemble_scores[6][5]/num_simulations*100,2),round(assemble_scores[6][6]/num_simulations*100,2)])
    print(score_matrix) 
    #calculate expected Pts and print a summary
    home_xPts = (home_win_probability / 100) * 3.0 + (draw_probability / 100) * 1.0 + (away_win_probability / 100) * 0.0
    away_xPts = (away_win_probability / 100) * 3.0 + (draw_probability / 100) * 1.0 + (home_win_probability / 100) * 0.0
    print ("**********************************")        
    print ("*                                *")       
    print ("*             RESUMEN            *")
    print ("*                                *")
    print ("**********************************")
    print(f"Probabilidad de ganar (%) de <<{input_home_team}>>:", home_win_probability, "xPts =", round(home_xPts,2))
    print(f"Probabilidad de ganar (%) de <<{input_away_team}>>:", away_win_probability, "xPts =", round(away_xPts,2))
    print("Probabilidad de empate (%):", draw_probability)
    print("Maximo de goles anotados por un equipo", max_score-1)
    #Creamos una recomendación
    if home_win_probability > away_win_probability:
        print("Recomendación: Apostar por el equipo local")
        return 0
    elif home_win_probability < away_win_probability:
        print("Recomendación: Apostar por el equipo visitante")
        return 1
    elif abs(home_win_probability-away_win_probability)< 10:
        print("Recomendación: Apostar por el empate")
        return 2
    else:
        print("Recomendación: Apostar por el empate")
        return 2
