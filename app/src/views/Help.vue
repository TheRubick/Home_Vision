<template>
<div/>
<ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        
        <ion-buttons slot="start">
        <ion-back-button text="HOME" default-href="/home"> </ion-back-button>
        </ion-buttons>
        <ion-title >Help</ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content>
        <ion-card>
          <ion-item>
            <ion-icon :icon="pin" slot="start"></ion-icon>
            <ion-label>Live Stream</ion-label>
          </ion-item>

          <ion-card-content>
            By selecting the live stream icon will start a live stream from the camera connected to the system so you can watch a live feed for the camera scene.
          </ion-card-content>
        </ion-card>

        <ion-card>
          <ion-item>
            <ion-icon :icon="pin" slot="start"></ion-icon>
            <ion-label>Find Object</ion-label>
          </ion-item>

          <ion-card-content>
              By selecting the find object icon will open the find object page from which you can select a certain object to search for in the camera scene. After pressing the find button a picture of the camera scene will be displayed with the object in a square box.          </ion-card-content>
        </ion-card>

        <ion-card>
          <ion-item>
            <ion-icon :icon="pin" slot="start"></ion-icon>
            <ion-label>Add Face</ion-label>
          </ion-item>

          <ion-card-content>
              By selecting the add face icon will open the add face page from which you can add a new person’s face so that the system can identify after that.
              Enter your name and then you will be asked to take 6 photos so you should stand in front of the camera and press take photo, the photo will be displayed after each photo you take. If you stop the process and start taking the photos from the beginning you can click cancel.
           </ion-card-content>
        </ion-card>

        <ion-card>
          <ion-item>
            <ion-icon :icon="pin" slot="start"></ion-icon>
            <ion-label>Settings</ion-label>
          </ion-item>

          <ion-card-content>
                By selecting the add settings this will open the settings page from which you can:<br/>
                - Enable face recognition: Sends you an email when a known or unknown person appears.<br/>
                - Enable motion detection: Sends you an email when any motion happens in the camera scene.<br/>
                - Delete a person from the system so that the system can’t recognize him/her anymore.<br/>
                - Enter the mail you want the app to send its notifications and alerts.<br/>
                - Select a person and an object that when both appear in the camera scene the app alerts you like your child carrying a knife.
          </ion-card-content>
        </ion-card>

        <ion-card>
          <ion-item>
            <ion-icon :icon="pin" slot="start"></ion-icon>
            <ion-label>Track Object</ion-label>
          </ion-item>

          <ion-card-content>
              By selecting the track object icon will open the track object page, then a live stream will open and you are asked to select two points on the live stream (the upper left corner of the object and the second point is the lower right corner) of the object you want to track. When you click stop tracking this will stop the object tracking, If the object disappears from the scene the app will send you mail that the object disappeared from the scene.

           </ion-card-content>
        </ion-card>
    </ion-content>
  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar} from '@ionic/vue';


export default {
  name: 'Help',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonBackButton
  }
}
</script>