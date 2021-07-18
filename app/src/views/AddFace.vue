<template>
<div/>
<ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        
        <ion-buttons slot="start">
        <ion-back-button text="HOME" default-href="/home"> </ion-back-button>
        </ion-buttons>
        <ion-title >Add Face </ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content>
        <ion-input v-show="show_name_items" v-model="personName" placeholder="Enter Your Name"></ion-input>
        <ion-button v-show="show_name_items" expand="block" size="large" fill="outline" shape="round" 
                  color="secondary" @click="saveName()">Save</ion-button>
        <ion-text v-show="!show_name_items" color="secondary">
          <h5>Stand in front of the camera and make sure your face is centered to the camera.
          </h5>
        

        <img v-if="showImg && first" v-bind:src="backend_path+'/take_photo'"/>
        <img v-if="showImg && second" v-bind:src="backend_path+'/take_photo2'"/>
        <img v-if="showImg && third" v-bind:src="backend_path+'/take_photo3'"/>
        <img v-if="showImg && fourth" v-bind:src="backend_path+'/take_photo4'"/>
        <img v-if="showImg && fifth" v-bind:src="backend_path+'/take_photo5'"/>
        <img v-if="showImg && sixth" v-bind:src="backend_path+'/take_photo6'"/>

        <ion-row >
          <ion-col>
              <ion-button v-show="!show_name_items && !returnHome"  size="large" fill="outline" shape="round" 
                 color="secondary" @click="takePhoto()">take photo ({{counter}})</ion-button>
              <ion-button v-show="!returnHome && !disableCancel"  size="large" fill="outline" shape="round" 
                     color="secondary" @click="cancel()" href="/home/addface">cancel</ion-button>  
              <ion-button v-show="returnHome"  size="large" fill="outline" shape="round" 
                      color="secondary" href="/home">Go home</ion-button>          
          </ion-col>
        </ion-row >
        
        
        </ion-text>
    </ion-content>
  </ion-page>
</template>
<script>
import {IonInput,IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar} from '@ionic/vue';

import axios from 'axios';
const saveNamePath = "/save_name";
const cancelPath = "/cancel_faces";

export default {
  name: 'AddFace',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonBackButton,
    IonInput
  },
  data(){
    return{
      returnHome:false,
      first:false,
      second:false,
      third:false,
      fourth:false,
      fifth:false,
      sixth:false,
      showImg: false,
      faceImgs: null,
      personName: '',
      show_name_items: true,
      temp:null,
      backend_path:this.$hostName,
      counter:6,
      disableTake:false,
      disableCancel:true,
    }
  },
  methods:{
    saveName(){
      this.show_name_items=false
      var payload = {
            Name:this.personName
          }
      axios.post(this.$hostName+saveNamePath,payload)
      .catch(err => console.log(err));
      console.log(this.personName);
    },
    takePhoto(){
      this.showImg=true;
      this.disableCancel=false;
      this.counter=this.counter-1;
      if(this.counter==5){
        this.third=false;
        this.first=true;
        this.second=false;
        this.fourth=false;
        this.fifth=false;
        this.sixth=false;
      }
      if(this.counter==4){
        this.first=false;
        this.second=true;
        this.third=false;
        this.fourth=false;
        this.fifth=false;
        this.sixth=false;
      }
      console.log(this.counter);
      if(this.counter==3){
        this.first=false;
        this.second=false;
        this.third=true;
        this.fourth=false;
        this.fifth=false;
        this.sixth=false;
      }
      if(this.counter==2){
        this.first=false;
        this.second=false;
        this.third=false;
        this.fourth=true;
        this.fifth=false;
        this.sixth=false;
      }
      if(this.counter==1){
        this.first=false;
        this.second=false;
        this.third=false;
        this.fourth=false;
        this.fifth=true;
        this.sixth=false;
      }
      if(this.counter==0){
        this.first=false;
        this.second=false;
        this.third=false;
        this.fourth=false;
        this.fifth=false;
        this.sixth=true;
        this.returnHome=true;
      }
      this.$forceUpdate();
    },
    cancel(){
      this.counter=3;
      this.first=false;
      this.second=false;
      this.third=false;
      axios.get(this.$hostName+cancelPath)
      .catch(err => console.log(err));
      this.showImg=false;
      this.forceUpdate();
    }
  }
}
</script>