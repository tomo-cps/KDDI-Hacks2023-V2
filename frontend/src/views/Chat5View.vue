<template>
  <v-row justify="center">
    <v-col cols="5" class="my-6">
      <h2>2023年度 KDDIハッカソン学会 &nbsp; 会場:クサヤ温泉</h2>
      <v-card class="pa-2 my-6">
        <v-img :src="receivedImage" alt="WordCloud Image" v-if="receivedImage" />
        <v-card-title class="headline mb-0" style="white-space: pre-line;">
          Twitterにおける共通の関心を持つユーザのレコメンド
        </v-card-title>
        <v-card-subtitle class="subtitle-1">
          貴志 将考
        </v-card-subtitle>
        <v-card-text>
          キーワード：
          <br>
          レコメンド
          <br>
          ユーザ
          <br>
          検索
          <br>
          コミュニティ
          <br>
          Twitter
          <br>
          抽出
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
  name: 'Chat5View',
  components: {
    ChatPage,
  },
  data() {
    return {
      receivedImage: "/images/hoge.png",
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

<style scoped>
.balloon_l,
.balloon_r {
  margin: 10px 0;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
}

.balloon_r {
  justify-content: flex-end;
}

.face_icon img {
  width: 80px;
  height: auto;
}

.balloon_r .face_icon {
  margin-left: 25px;
}

.balloon_l .face_icon {
  margin-right: 25px;
}

.balloon_r .face_icon {
  order: 2 !important;
}

.says {
  max-width: 300px;
  display: flex;
  flex-wrap: wrap;
  position: relative;
  padding: 10px;
  border-radius: 12px;
  background: #8ee7b6;
  box-sizing: border-box;
  margin: 0 !important;
  line-height: 1.5;
  /* align-items: center; */
}

.says p {
  margin: 8px 0 0 !important;
}

.says p:first-child {
  margin-top: 0 !important;
}

.says:after {
  content: "";
  position: absolute;
  border: 10px solid transparent;
  margin-top: -3px;
}

.balloon_l .says:after {
  left: -26px;
  border-right: 22px solid #8ee7b6;
}

.balloon_r .says:after {
  right: -26px;
  border-left: 22px solid #8ee7b6;
}
</style>
