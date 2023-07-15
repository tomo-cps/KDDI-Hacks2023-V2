<template>
  <v-row justify="center">
    <v-col cols="5" class = "my-6">
    <h2>2023年度  KDDIハッカソン学会  &nbsp; 会場:クサヤ温泉</h2>
    <v-card class="pa-2 my-6">
      <v-img :src="receivedImage" alt="WordCloud Image" v-if="receivedImage" />
    <v-card-title class="headline mb-0" style="white-space: pre-line;">
      超塑性ナイロン系アロイの構造と物性
    </v-card-title>
    <v-card-subtitle class="subtitle-1">
      熱海智也
    </v-card-subtitle>
    <v-card-text>
      キーワード：
      <br>
      6ナイロン(PA)
      <br>
      エチレン・メタクリル酸グリシジル(EGMA)
      <br>
      アロイ(NOVA)
      <br>
      超塑性
      <br>
      機械的特性
      <br>
      高温変形
    </v-card-text>
  </v-card>
    </v-col>
    <v-col cols="5">
      <ChatPage @imageData="handleImageData" />
    </v-col>
  </v-row>
</template>

<script>
import { defineComponent } from 'vue';

// Components
import ChatPage from '@/components/ChatPage.vue';

export default defineComponent({
  name: 'Chat3View',
  components: {
    ChatPage,
  },
  data() {
    return {
      receivedImage: "/images/material.png",
    };
  },
  mounted() {
  },
  methods: {
    handleImageData(imageBinary) {
      this.receivedImage = imageBinary;
    },
  }
}
);
</script>