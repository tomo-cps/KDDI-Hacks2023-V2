<template>
  <v-row justify="center">
    <v-col cols="5" class = "my-6">
    <h2>2023年度  KDDIハッカソン学会  &nbsp; 会場:クサヤ温泉</h2>
    <v-card class="pa-2 my-6">
      <v-img :src="receivedImage" alt="WordCloud Image" v-if="receivedImage" />
    <v-card-title class="headline mb-0" style="white-space: pre-line;">
      深層学習による画像認識を用いたコンクリート建造物の変状検出に関する研究
    </v-card-title>
    <v-card-subtitle class="subtitle-1">
      青山亘佐
    </v-card-subtitle>
    <v-card-text>
      キーワード：
      <br>
      コンクリート構造
      <br>
      橋梁検査
      <br>
      深層学習
      <br>
      画像認識
      <br>
      物体検出
      <br>
      畳み込みニューラルネットワーク（CNN）
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
import ChatPage from '@/components/ChatPage.vue';

export default defineComponent({
  name: 'Chat1View',
  components: {
    ChatPage,
  },
  data() {
    return {
      receivedImage: "/images/it.png",
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