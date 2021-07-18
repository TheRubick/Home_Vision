<template>
<div/>
<ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        
        <ion-buttons slot="start">
        <ion-back-button text="HOME" default-href="/home"> </ion-back-button>
        </ion-buttons>
        <ion-title >Settings </ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list>
        <ion-item>
          <ion-label>Face Recognition</ion-label>
          <ion-toggle
            v-model="current_settings[0]"
            @ionChange="face_toggled"
            :checked="current_settings[0]">
          </ion-toggle>
        </ion-item>

          <ion-item>
          <ion-label>Motion Detection</ion-label>
          <ion-toggle
            v-model="current_settings[1]"
            @ionChange="motion_toggeled"
            :checked="current_settings[1]">
          </ion-toggle>
        </ion-item>

        </ion-list>
      </ion-content>
  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar,IonLabel, IonList, IonItem, IonToggle} from '@ionic/vue';

import axios from 'axios';
const currentSettingsPath = "/current_settings";
const updateSettingsPath = "/update_settings";

export default {
  name: 'Settings',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonBackButton,
    IonLabel,
    IonList,
    IonItem,
    IonToggle
  },
  data(){
    return{
      current_settings:[]
    }
  },
  methods:{
    face_toggled(){
      var payload = {
            Current_Settings:this.current_settings
      }
      axios.post(this.$hostName+updateSettingsPath, payload)
      .catch(err => console.log(err))
    },
    motion_toggeled(){
      var payload = {
            Current_Settings:this.current_settings
      }
      axios.post(this.$hostName+updateSettingsPath, payload)
      .catch(err => console.log(err))
    }
  },
  beforeMount(){
      axios.get(this.$hostName+currentSettingsPath)
      .then(res => {this.current_settings[0]=res.data[0];
          this.current_settings[1]=res.data[1];
          })
      .catch(err => console.log(err))
  }
}
</script>