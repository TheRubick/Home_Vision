<template>
<div/>
<ion-page>
      <ion-header :translucent="true">
      <ion-toolbar align-title="center">
        <ion-title  >Start</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-item>
        <ion-label position="stacked">Enter Ip Address</ion-label>
      <ion-input v-model="ip"></ion-input>
    </ion-item>
      <ion-button   expand="block" size="large" fill="outline" 
      shape="round" @click="enter()" color="secondary" >Enter</ion-button>
    
    </ion-content>
  </ion-page>
</template>
<script>
import { IonContent,  IonPage, IonHeader, IonTitle,
     IonToolbar,IonLabel, IonInput, IonItem } from '@ionic/vue';


export default {
  name: 'Start',
  components: {
    IonContent,
    IonPage,
    IonHeader, 
    IonTitle,
    IonToolbar,
    IonLabel, 
    IonInput, 
    IonItem 

  },
  data(){
    return{
      ip:''
    }
  },
  methods:{
    enter(){
      console.log(this.ip)
      //this.$hostName = "http://"+this.ip+":5000";
      this.$changeHostName(this.ip)
      console.log(this.$hostName);
        this.$router.push({name:"Home"})
;      
    }
  }
}
</script>