<template>
<div/>
<ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        
        <ion-buttons slot="start">
        <ion-back-button text="HOME" default-href="/home" v-on:click="stop" > </ion-back-button>
        </ion-buttons>
        <ion-title >Live Stream </ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content>
        <img v-bind:src="backend_path+'/video_feed'"/>
    </ion-content>
  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar} from '@ionic/vue';
import axios from 'axios';
const stop_feed_path = "/stop_feed";

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
      temp:null,
      backend_path:this.$hostName
    }
  },
  methods:{
    stop(){
      axios.get(this.$hostName+stop_feed_path)
      .then(
        res => {
        this.temp = res ;
        })
      .catch(err => console.log(err));
      this.$router.push({name:"Home"})
    }
  }
}
</script>