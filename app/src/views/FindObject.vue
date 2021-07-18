<template>
<div/>
<ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        
        <ion-buttons slot="start">
        <ion-back-button text="HOME" default-href="/home"> </ion-back-button>
        </ion-buttons>
        <ion-title >Find Object </ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content>
      <ion-list>
        <ion-list-header>
          <ion-label>
            {{msg}}
          </ion-label>
        </ion-list-header>

        <ion-item>
          <ion-label>Gender</ion-label>
          <ion-select v-model="objectId" placeholder="Select One">
            <ion-select-option value="0">Backpack</ion-select-option>
            <ion-select-option value="1">Headphones</ion-select-option>
            <ion-select-option value="2">Knife</ion-select-option>
            <ion-select-option value="3">Laptop</ion-select-option>
            <ion-select-option value="4">Mobile Phone</ion-select-option>
            <ion-select-option value="5">Remote Control</ion-select-option>
            <ion-select-option value="6">Scissors</ion-select-option>
            <ion-select-option value="7">Watch</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>
      <ion-button expand="block" size="large" fill="outline" 
      shape="round" @click="find()" color="secondary">Find</ion-button>
      <img v-if="sent"  v-bind:src="backend_path+'/find_object'"/>
    </ion-content>

  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar, IonItem, 
  IonLabel, 
  IonList,
  IonListHeader,
  IonSelect,
  IonSelectOption,
  IonButton
  } from '@ionic/vue';


export default {
  name: 'FindObject',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonBackButton,
    IonItem, 
    IonLabel, 
    IonList,
    IonListHeader,
    IonSelect,
    IonSelectOption,
    IonButton
  },
  data(){
    return{
      objectId:-1,
      msg:"Select An Object",
      sent:false,
      backend_path:this.$hostName,
      dummy:0
    }
  },
  methods:{

    find(){
       this.sent = false;

  // If you like promises better you can
  // also use nextTick this way
  
      if (this.objectId===-1){
        //
        this.msg = "No Object is Selected"
      }
      else{
        this.msg = "Select An Object";
        this.sent = true; 
      }
    }

  }
  
}
</script>