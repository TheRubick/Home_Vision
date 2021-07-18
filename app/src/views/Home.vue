<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title >Home Page </ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content>
        <img src="./logo.png"/>
          <ion-grid>
              <ion-row >
                <ion-col>
                  <ion-button expand="block" size="large" fill="outline" shape="round" 
                  color="secondary" href="/home/livestream">Live Stream</ion-button>
                </ion-col>
                <ion-col>
                  <ion-button expand="block" size="large" color="secondary" fill="outline" shape="round" 
                  href="/home/findobject">Find object</ion-button>
                </ion-col>
              </ion-row>
              <ion-row >
                <ion-col>
                  <ion-button expand="block" size="large" fill="outline" shape="round" color="secondary"
                  href="/home/addface">Add face</ion-button>
                </ion-col>
                <ion-col>
                  <ion-button expand="block" size="large" color="secondary" fill="outline" shape="round"
                  href="/home/settings">Settings</ion-button>
                </ion-col>
              </ion-row>
              <ion-row >
              <ion-col size="3">
                  
                </ion-col>
                <ion-col>
                  <ion-button expand="block" size="large" fill="outline" shape="round" color="secondary"
                  href="/home/help">help</ion-button>
                </ion-col>
                <ion-col size="3">
                  
                </ion-col>
              </ion-row>
          </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script >
import {IonContent, IonHeader, IonPage, IonTitle,
     IonToolbar,IonCol, IonGrid, IonRow} from '@ionic/vue';
import { defineComponent } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
//const path = "http://192.168.1.109:5000/test";
const path = "/test";

export default defineComponent({
  name: 'Home',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonCol,
    IonGrid,
    IonRow 
  },
  data(){
    return {
      todos:[],
      data:"no data",
      temp:null
    }
  },
  created(){
    axios.get(this.$hostName+path)
      .then(
        res => {this.data = res.data.res;
        console.log(this.data)
        })
      .catch(err => console.log(err));
  },
  methods: {
    liveStream(){
      this.$router.push({name:'LiveStream'});
      //location.reload();
    }
  },
  setup() {
      const router = useRouter();
      return { router };
    }
});
</script>

<style scoped>
#container {
  text-align: center;
  
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

#container strong {
  font-size: 20px;
  line-height: 26px;
}

#container p {
  font-size: 16px;
  line-height: 22px;
  
  color: #8c8c8c;
  
  margin: 0;
}

#container a {
  text-decoration: none;
}
</style>