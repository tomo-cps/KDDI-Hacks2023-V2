<template>
    <v-app>
        <v-main>
            <v-container>
                <v-row class="text-center">
                    <v-col cols="12">
                        <v-card class="mx-auto my-6" elevation="2" max-width="500" color="grey lighten-5">
                            <v-card-title>Chat Bot</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text><v-row>
                                    <v-col cols="12">
                                        <v-container ref="scrollTarget" style="height: 450px" class="overflow-y-auto">
                                            <v-row v-for="(msg, i) in messages" :key="i" dense>
                                                <v-col v-if="msg.ws_key != ws_key">
                                                    <div class="balloon_l">
                                                        <div class="face_icon">
                                                            <v-avatar :color="msg.avatar_color">
                                                                <span class="white--text">
                                                                    {{ msg.name }}
                                                                </span>
                                                            </v-avatar>
                                                        </div>
                                                        <p class="says">
                                                            {{ msg.message }}
                                                        </p>
                                                    </div>
                                                </v-col>
                                                <v-col v-else>
                                                    <div class="balloon_r">
                                                        <div class="face_icon">
                                                            <v-avatar :color="msg.avatar_color">
                                                                <span class="white--text">
                                                                    {{ msg.name }}
                                                                </span>
                                                            </v-avatar>
                                                        </div>
                                                        <p class="says">
                                                            {{ msg.message }}
                                                        </p>
                                                    </div>
                                                </v-col>
                                            </v-row>
                                        </v-container>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="3">
                                        <v-text-field label="名前" v-model="name" clearable></v-text-field>
                                    </v-col>
                                    <v-col>
                                        <v-text-field autofocus label="メッセージ" v-model="message" clearable
                                            :return-key="false" @input="updateButtonColor"></v-text-field>
                                    </v-col>
                                </v-row>
                                <v-btn class="info" small :color="buttonColor" @click="send_onClick">
                                    <v-icon>mdi-play</v-icon>送信
                                </v-btn>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>
<script>
import { defineComponent } from 'vue';

// Components
import axios from 'axios';

export default defineComponent({
    name: 'Chat1View',
    data() {
        return {
            imagePath: null,
            imageBinary: null,
            name: "とも",
            message: "質問はここからどうぞ",
            messages: [],
            buttonColor: 'black',
            ws_key: null,
            avatar_color: "",
            path: "",
        };
    },
    created: function () {
        // アバターの色をランダムに決める
        let random_color = "#";
        for (var i = 0; i < 6; i++) {
            random_color += "0123456789abcdef"[(16 * Math.random()) | 0];
        }
        this.avatar_color = random_color;
        const currentURL = window.location.href;
        const regex = /\/([^/]+)$/;
        const match = regex.exec(currentURL);
        if (match && match.length > 1) {
            const path = match[1];
            this.path = path
        }
    },
    mounted() {
    },
    methods: {
        updateButtonColor() {
            if (this.message.trim() !== '') {
                this.buttonColor = 'black';
            } else {
                this.buttonColor = '#808080';
            }
        },
        send_onClick: async function () {
            if (this.message == "") return;
            // ユーザのメッセージをチャットボックスに追加
            this.messages.push({
                ws_key: this.ws_key,
                avatar_color: this.avatar_color,
                message: this.message,
                name: this.name,
            });
            axios.defaults.withCredentials = true;
            // FastAPIサーバーにHTTP POSTリクエストを送信
            axios
                .post('https://gmc.cps.akita-pu.ac.jp/ask/', {
                    name: this.name,
                    path: this.path,
                    question: this.message,
                })
                .then((response) => {
                    this.messages.push({
                        ws_key: this.ws_key,
                        avatar_color: this.avatar_color,
                        message: response.data.answer,
                        name: 'Bot',
                    });
                    this.imagePath = 'data:image/png;base64,' + response.data.wordcloud;
                    this.sendImageToParent(this.imagePath);
                    // console.log(imageBinary)
                })
                .catch((error) => {
                    console.error(error);
                });
            this.message = '';
        },
        sendImageToParent(imageBinary) {
            this.$emit('imageData', imageBinary); // イメージのバイナリデータを親コンポーネントに送信する
        },
        // scrollToEnd() {
        //     this.$nextTick(() => {
        //         const chatLog = this.$refs.scrollTarget;
        //         if (!chatLog) return;
        //         chatLog.scrollTop = chatLog.scrollHeight;
        //     });
        // },
    },
});
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