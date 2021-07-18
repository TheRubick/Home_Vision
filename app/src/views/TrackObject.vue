<template>
<div/>
<ion-page>
    <ion-header ref="head" :translucent="true" >
      <ion-toolbar >
        
        <ion-buttons slot="start">
        <ion-back-button text="HOME" default-href="/home" v-on:click="stop" > </ion-back-button>
        </ion-buttons>
        <ion-title >Track Object</ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content  >
    <img v-if="!stream" @click="getCoordinates($event)" ref="theImage" v-bind:src="backend_path+'/track_object'"/> 
    <img v-if="stream" v-bind:src="backend_path+'/video_feed'"/>
    <ion-button disabled v-show="!enable" expand="block" size="large" fill="outline" 
      shape="round" @click="track()" color="secondary" >Track</ion-button>
      <ion-button  v-show="enable" expand="block" size="large" fill="outline" 
      shape="round" @click="track()" color="secondary" >Track</ion-button>
    <ion-card>
    <ion-card-content v-show="show">
      X axis from {{x1}}% to {{x2}}%
      Y axis from {{y1}}% to {{y2}}%
    </ion-card-content>
    
  </ion-card>
    </ion-content>
  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar,IonCard, IonCardContent,IonButton} from '@ionic/vue';
import axios from 'axios';
const cooords_path = "/track_coords";
const stop_feed_path = "/stop_feed";
//
export default {
  name: 'TrackObject',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonBackButton,
    IonCard, 
    IonCardContent,
    IonButton
  },
  data(){
      return{
          backend_path:this.$hostName,
          x1:-1,
          x2:-1,
          y1:-1,
          y2:-1,
          myImage:'',
          show:false,
          enable: false,
          stream: false 
      }
  },
  methods:{
      getCoordinates(event){
        // This output's the X coord of the click
        //console.log(event.clientX);
        // This output's the Y coord of the click
        //console.log(event.clientY);
        //console.log( this.$refs.theImage.clientHeight)
        //console.log( this.$refs.head.$el.clientHeight)
        //console.log( this.$refs.theImage.clientWidth)
        this.show = false;
        if(this.x1 ===-1){
            this.x1 = (event.clientX/this.$refs.theImage.clientWidth).toFixed(2);
            this.y1 = ((event.clientY-this.$refs.head.$el.clientHeight)/this.$refs.theImage.clientHeight).toFixed(2);
            console.log(this.x1)
            console.log(this.y1)
        }
        else{
            this.x2 = (event.clientX/this.$refs.theImage.clientWidth).toFixed(2);
            this.y2 = ((event.clientY-this.$refs.head.$el.clientHeight)/this.$refs.theImage.clientHeight).toFixed(2);
            console.log(this.x2)
            console.log(this.y2)
            this.enable = true;
            console.log(this.enable);
        }
    },
    track(){
        if (this.x1 > this.x2) {
            let temp = this.x2
            this.x2 = this.x1
            this.x1 = temp
        }
        if (this.y1 > this.y2) {
            let temp = this.y2
            this.y2 = this.y1
            this.y1 = temp
        }
        this.show = true;
        var payload = {
        x1:this.x1,
        y1:this.x1,
        x2:this.x2,
        y2:this.y2
        }
        axios.post(this.backend_path+cooords_path,payload)
        .then(res =>{
            console.log(res);
            if (res.data.res == "success") {
                this.stream= true;
            }
        })
    },
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