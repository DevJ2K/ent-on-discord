async def dropdown_callback(interaction: discord.Interaction):

        print(dropdownOption.values[0])
        
        if dropdownOption.values[0] == "edt":
            await edtButton_callback(interaction=interaction)
        elif dropdownOption.values[0] == "allDevoirs": 
            await allDevoirsButton_callback(interaction=interaction)
        elif dropdownOption.values[0] == "lastNotes":
            await lastNotesButton_callback(interaction=interaction)
        elif dropdownOption.values[0] == "moyenneG": 
            await moyenneGeneraleButton_callback(interaction=interaction)
        elif dropdownOption.values[0] == "allMoyennes": 
            await allMoyennesButton_callback(interaction=interaction)
            
        

    option1 = SelectOption(label="Emploi Du Temps", value="edt")
    option2 = SelectOption(label="Devoirs", value="allDevoirs")
    option3 = SelectOption(label="Dernières Notes", value="lastNotes")
    option4 = SelectOption(label="Moyenne Générale", value="moyenneG")
    option5 = SelectOption(label="Toutes Vos Moyennes", value="allMoyennes")

    dropdownOption = Select(placeholder="Que souhaitez-vous obtenir ?", options=[option1, option2, option3, option4, option5], max_values=1)   
    dropdownOption.callback = dropdown_callback

    allButtonsView.add_item(faireUneDemandeButton)
    allButtonsView.add_item(dropdownOption)