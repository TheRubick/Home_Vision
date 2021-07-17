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
        
    </ion-content>
  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar} from '@ionic/vue';


export default {
  name: 'FindObject',
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