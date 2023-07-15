<template>
  <v-row justify="center">
    <v-col cols="5" class = "my-6">
    <h2>2023年度  KDDIハッカソン学会  &nbsp; 会場:クサヤ温泉</h2>
    <v-card class="pa-2 my-6">
      <v-img :src="receivedImage" alt="WordCloud Image" v-if="receivedImage" />
    <v-card-title class="headline mb-0" style="white-space: pre-line;">
      深層畳み込みニューラルネットワークに基づくコンクリート表面のひび割れ検出システム
    </v-card-title>
    <v-card-subtitle class="subtitle-1">
      野村泰稔
    </v-card-subtitle>
    <v-card-text>
      キーワード：
      <br>
      深層畳み込みニューラルネットワーク (Deep convolutional neural network)
      <br>
      表面検査 (Surface inspection)
      <br>
      ひび割れ検出 (Crack detection)
      <br>
      イメージ処理 (Image processing)
      <br>
      機械学習 (Machine learning)
      <br>
      パターン認識 (Pattern recognition)
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
  name: 'Chat4View',
  components: {
    ChatPage,
  },
  data() {
    return {
      receivedImage: "/images/deeplearning.png",
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