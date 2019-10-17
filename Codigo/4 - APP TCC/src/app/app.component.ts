import { Component } from '@angular/core';

import { Platform } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { AndroidPermissions } from '@ionic-native/android-permissions/ngx';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss']
})
export class AppComponent {
  public appPages = [
    {
      title: 'Home',
      url: '/home',
      icon: 'home'
    },
    {
      title: 'List',
      url: '/list',
      icon: 'list'
    }
  ];

  constructor(
    private platform: Platform,
    private splashScreen: SplashScreen,
    private statusBar: StatusBar,
    private androidPermissions: AndroidPermissions
  ) {
    this.initializeApp();
  }

  initializeApp() {
    this.platform.ready().then(() => {
      if(this.platform.is('cordova')) {
        // Checa e, se necessário, requisita permissão para usar localização do dispositivo
        this.androidPermissions.checkPermission(this.androidPermissions.PERMISSION.CAMERA).then((result) => {
          if(!result.hasPermission) {
            this.androidPermissions.requestPermission(this.androidPermissions.PERMISSION.CAMERA)
          }
        });
      }

      this.statusBar.styleDefault();
      this.splashScreen.hide();
    });
  }

}
