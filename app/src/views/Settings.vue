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

                <ion-item>
          <ion-label>Select Person</ion-label>
          <ion-select :value="selectedFace"
          @ionChange="selectedFace= $event.target.value" placeholder="Person">
            <ion-select-option v-for="face in faces" :key="face" :value="face" 
             >{{face}}</ion-select-option>
          </ion-select>
                <ion-button  expand="block"  fill="outline" 
              shape="round" @click="deleteFace()" color="secondary">Delete</ion-button>
        </ion-item>
        <ion-item>
          <ion-label>Default Label</ion-label>
          <ion-input v-model="email" inputmode="email" placeholder="Enter Email"></ion-input>
           <ion-button  size="small"  fill="outline" 
              shape="round"  @click="changeMail()" color="secondary">change E-Mail</ion-button>
        </ion-item>
        <ion-item>
          <ion-label>Select Person</ion-label>
          <ion-select :value="useCaseFace"
          @ionChange="useCaseFace= $event.target.value" placeholder="Person">
            <ion-select-option v-for="face in faces" :key="face" :value="face" 
             >{{face}}</ion-select-option>
          </ion-select>
          <ion-label>Select Item</ion-label>
          <ion-select :value="useCaseItem"
          @ionChange="useCaseItem= $event.target.value" placeholder="Item">
            <ion-select-option v-for="item in items" :key="item.id" :value="item.id" 
             >{{item.name}}</ion-select-option>
          </ion-select>
        </ion-item>
        <ion-button  expand="block"  fill="outline" 
              shape="round" @click="useCase()" color="secondary">{{useCaseBtnTxt}}</ion-button>
        </ion-list>
    </ion-content>
  </ion-page>
</template>
<script>
import {IonButtons, IonBackButton, IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar,IonLabel, IonList, IonItem, IonToggle, IonButton,IonSelect,
  IonSelectOption,IonInput} from '@ionic/vue';

import axios from 'axios';
const currentSettingsPath = "/current_settings";
const updateSettingsPath = "/update_settings";
const get_faces_path = "/get_faces";
const delete_face_path = "/delete_face";
const change_mail_path = "/change_mail";
const get_mail_path = "/get_mail";
const set_use_case_path = "/set_use_case"
const get_use_case_path = "/get_use_case"

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
    IonToggle,
    IonButton,
    IonSelect,
    IonSelectOption,
    IonInput
  },
  data(){
    return{
      current_settings:[],
       faces:null,
       selectedFace:"",
       email:"",
       useCaseItem:"",
       useCaseFace:"",
       enableCaseFlag:false,
       useCaseBtnTxt:"Enable",
       items:[
         {
           id: 0,
           name: "Backpack"
         },
         {
           id: 1,
           name: "Headphones"
         },
         {
           id: 2,
           name: "Knife"
         },
         {
           id: 3,
           name: "Laptop"
         },
         {
           id: 4,
           name: "Mobile Phone"
         },
         {
           id: 5,
           name: "Remote Control"
         },
         {
           id: 6,
           name: "Scissors"
         },
         {
           id: 7,
           name: "Watch"
         }
       ]
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
    },
    deleteFace(){
      if (this.selectedFace !=="") {
        console.log(this.selectedFace)
        var payload = {
          name:this.selectedFace
        }
        axios.post(this.$hostName+delete_face_path,payload)
        .then(res =>{
            console.log(res);
            this.selectedFace = "";
            axios.get(this.$hostName+get_faces_path)
            .then(res => {this.faces=res.data;
              })
            .catch(err => console.log(err))
        })
        .catch(err => console.log(err))
      }
      
    },
    changeMail(){
      var payload = {
        email: this.email
      }
      axios.post(this.$hostName+change_mail_path,payload)
        .then(res =>{
            console.log(res);
            this.getMail()
        })
    },
    getMail(){
      axios.get(this.$hostName+get_mail_path)
        .then(res =>{
            this.email = res.data.email;
        })
    },
    useCase(){
      this.enableCaseFlag = !this.enableCaseFlag;
      var payload =  {
        flag: this.enableCaseFlag,
        item: this.useCaseItem,
        face: this.useCaseFace
      }
      axios.post(this.$hostName+set_use_case_path,payload)
      .then(res=>{
        console.log(res);
        this.getUseCase();
      })
    },
    getUseCase(){
      axios.get(this.$hostName+get_use_case_path)
      .then(res => {
        this.enableCaseFlag = res.data.flag;
        if (this.enableCaseFlag == true) {
          this.useCaseBtnTxt = "Disable"
          this.useCaseItem = res.data.item;
          this.useCaseFace = res.data.face;
        }
        else{
          this.useCaseBtnTxt = "Enable";
          this.useCaseItem = res.data.item;
          this.useCaseFace = res.data.face;
        }
      })
    }
  },
  beforeMount(){
      axios.get(this.$hostName+currentSettingsPath)
      .then(res => {this.current_settings[0]=res.data[0];
          this.current_settings[1]=res.data[1];
          })
      .catch(err => console.log(err))
      axios.get(this.$hostName+get_faces_path)
      .then(res => {this.faces=res.data;
          })
      .catch(err => console.log(err))

      this.getMail();

      this.getUseCase()

  }
}
</script>