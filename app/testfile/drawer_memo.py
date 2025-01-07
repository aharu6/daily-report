if self.page.client_storage is not None:
    data = self.page.client_storage.get("timeline_data")
    print(data)
    
def reload_data_add_content(page,drawer):
    data = page.client_storage.get("timeline_datadata")
    if data is not None:
        for i in data:
            drawer.controls.append(
                ft.Row(
                    
                )
            )
            
            
        #もしくは
            drawer.controls.append(
                ft.NavigationDrawerDestination
            )
ReloadDataHandler.reload_data(self.page,self.reloadDrawer)

    #write時にclient_storageにデータを保存しているか