<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title >Blank </ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Blankkk</ion-title>
        </ion-toolbar>
      </ion-header>
    
      <div id="container">
        <strong>Ready to create an app? {{data}}</strong>
        <p>Start with Ionic <a target="_blank" rel="noopener noreferrer" href="https://ionicframework.com/docs/components">UI Components</a></p>
      </div>
    </ion-content>
  </ion-page>
</template>

<script >
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/vue';
import { defineComponent } from 'vue';
//import axios from 'axios';

//const path = "http://192.168.1.109:5000/test";
//const path = "/test";
export default defineComponent({
  name: 'Home',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar
  },
  data(){
    return {
      todos:[],
      data:"no data",
      
    }
  },
  /*created(){
    //axios.get('https://jsonplaceholder.typicode.com/todos?_limit=5')
    /*axios.get(this.$hostName+path)
      .then(
        res => {this.data = res.data.res;
        console.log(this.data)
        })
      .catch(err => console.log(err));
  }*/
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