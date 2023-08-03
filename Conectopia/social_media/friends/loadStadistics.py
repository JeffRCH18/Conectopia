#Required data models
from friends.models import Amistad
from usuarios.models import Usuarios
from usuarios.models import Gustos
from usuarios.models import GustosUsuarios

#Data manipulation libraries
import pandas as pd
import numpy as np

def getNewFriendsSuggestion(userID):

    userID = str(userID)
    print(userID)

    #Get the user list values
    usersList = Usuarios.objects.all()
    usersList = pd.DataFrame(list(usersList.values()))
    usersList = usersList.rename(columns= {'_id':'UsuarioID'})
    
    #Validate if the user is in the list
    usersList['delete_ind'] = usersList['UsuarioID'].apply(str).apply(lambda x : 'delete' if x == userID else 'keep')
    usersList = usersList[usersList['delete_ind'] == 'keep']
    print(usersList)

    #Get the information of current friends
    friends = Amistad.objects.all()
    friends = pd.DataFrame(list(friends.values()))

    if friends.empty:
        recommendation = usersList[['nombre','imagen']].head(3)
    else:
        #Validate if the users should be ignore as part of the recomendations. 
        
        friends['ignore_ind'] = np.where(
            friends['user1_id'] == userID,
            'Ignore',
            np.where(
                friends['user2_id'] == userID,
                'Ignore',
                'Keep'
            )
        )

        friends['merge_id'] = np.where(
            friends['ignore_ind'] == 'Ignore',
                np.where(
                    friends['user1_id'].apply(str) == userID,
                    friends['user2_id'],
                    friends['user1_id']
                ),
                'Delete'
        )

        friends = friends[['merge_id','ignore_ind']]
        friends = friends.drop_duplicates()
        
        print(friends)

        #Merge the data sets. 
        recommendation = pd.merge(usersList,friends,left_on='UsuarioID',right_on='merge_id',how='left').drop(columns=['merge_id'])
        recommendation = recommendation[~(recommendation['ignore_ind'] == 'Ignore')][['nombre','imagen']].head(3)
    
    recommendation = recommendation.to_json(orient='records')
    print(recommendation)
    

    return recommendation

def getNewPreferencesSuggestion(userID):

    userID = str(userID)

    preferences = Gustos.objects.all()
    preferences = pd.DataFrame(list(preferences.values()))

    print(preferences)

    #Getting all the items from the data base, do some manipulation to get only the information required. 
    preferencesUser = GustosUsuarios.objects.all()
    preferencesUser = pd.DataFrame(list(preferencesUser.values()))
    preferencesUser['is_User'] = preferencesUser['idUsuario_id'].apply(str).apply(lambda x: 1 if x == userID else 0)
    preferencesUser['idUsuario_id'] = 1
    preferencesUser = preferencesUser.groupby(['idGusto_id'],as_index=False)[['idUsuario_id','is_User']].sum()

    preferenceList = pd.merge(preferences,preferencesUser,left_on='_id',right_on='idGusto_id',how='left').drop(columns={'idGusto_id'})
    preferenceList['idUsuario_id'] = preferenceList['idUsuario_id'].fillna(0)
    preferenceList['is_User'] = preferenceList['is_User'].fillna(0)
    preferenceList = preferenceList.sort_values(by = 'is_User',ascending = False)
    preferenceList['_id'] = preferenceList['_id'].apply(str)
    preferenceList = preferenceList.rename(columns = {'_id':'gustoID'})
    
    preferenceList = preferenceList[preferenceList['is_User'] == 0][['gustoID','gusto','idUsuario_id']].rename(columns = {'idUsuario_id':'total_followers'})
    preferenceList = preferenceList.sort_values(by = 'total_followers',ascending = False)
    preferenceList = preferenceList.head(3)

    #Concert the list in a dictionary
    preferenceList = preferenceList.to_json(orient='records')
    print(preferenceList)
    return preferenceList