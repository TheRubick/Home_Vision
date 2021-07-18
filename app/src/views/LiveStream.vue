<template>
<div/>
<ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        
        <ion-buttons slot="start">
        <ion-back-button text="HOME" default-href="/home"> </ion-back-button>
        </ion-buttons>
        <ion-title >Live Stream </ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content>
        <img src="{{ url_for('http://127.0.0.1:5000/video_feed') }}"/>
    </ion-content>
  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar} from '@ionic/vue';
const path = "/video_feed";
import axios from 'axios';
export default {
  name: 'LiveStream',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonBackButton
  },
  data(){
    return{
      img:null
    }
  },
    onCreate(){
    axios.get(this.$hostName+path)
      .then(
        res => {this.img = res.data;
        console.log(res)
        })
      .catch(err => console.log(err));
  },
}
</script>