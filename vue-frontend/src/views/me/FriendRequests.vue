<template lang="">
<div style="overflow-x: hidden;">
  <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的好友申请</h3>
  <template v-if="userFriendsRequestID&&userFriendsRequestID.length"> 
  <el-row :gutter="20">
      <el-col :span="12" v-for="(row,index) in userFriendsRequest" :key="index" class="user-card"> 
        <!-- <div v-for="(fid, index) in userFriendsRequestID" :key="index"> -->
        <el-card shadow="hover">
          <div style="display: flex; align-items: center;">
            <img :src="row.data.iconUrl" style="width: 50px; height: 50px; border-radius: 50%;" @error="handleImageError"/>
            <div style="margin-left: 10px;">
               <p>用户ID:{{ userFriendsRequestID[index] }}</p>
              <p>用户名:{{ row.data.name }}</p>
              <!-- <p>
                IP地址:{{ row.data.ip }}
                <span v-if="row.data.ip == null" style="color: red; margin-right: 10px;">用户已登出</span>
              </p> -->
            </div>
          </div>
          <div style="margin-top:20px">
          <el-button plain type="success" icon="el-icon-check" @click='handleAgree(userFriendsRequestID[index])'>同意申请</el-button>
          <el-button plain type="danger" icon="el-icon-close" @click='handleRefuse(userFriendsRequestID[index],index)'>拒绝申请</el-button>
        </div>
        </el-card>
      <!-- </div> -->
      </el-col>
    </el-row>
  </template>
<div v-else class="emptyFriendsRequests">
  <el-empty description="暂无好友申请"></el-empty>
</div>
</div>
</template>
<script>
import { getFriendsRequest } from '@/api/collaborate'
import { handleFriendRequest } from '@/api/collaborate'
import { findById } from "@/api/user"
import config from "@/services/conf"
export default {
  name: "FriendsRequests",
  data() {
    return {
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
      userFriendsRequestID: [],
      userFriendsRequest: []
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      const id = localStorage.getItem('uid')
      getFriendsRequest(id).then(res => {
        this.userFriendsRequestID = res.fid;

        if (this.userFriendsRequestID) {
          console.log('用户好友请求的id列表', this.userFriendsRequestID)
          Promise.all(this.userFriendsRequestID.map(fid => {
            const fidObject = { id: fid };
            return findById(fidObject);
          }))
            .then(res => {
              this.userFriendsRequest = res
              console.log('好友请求列表的用户信息', this.userFriendsRequest)

              //设置用户头像
              this.userFriendsRequest = this.userFriendsRequest.map(user => {
                if (user.data.iconUrl) {

                  // 替换所有反斜杠为斜杠
                  let iconUrl = user.data.iconUrl.replace(/\\/g, '/');

                  // 移除 'App' 字符串
                  iconUrl = iconUrl.replace(/App/g, '');

                  // 拼接完整的 URL
                  // iconUrl = `${config.API_URL}/${iconUrl}`;

                  iconUrl = config.API_URL + iconUrl;

                  console.log('进行拼接', iconUrl)
                  return { ...user, data: { ...user.data, iconUrl } }; // 返回包含更新后的 iconUrl 的用户信息对象
                } else {
                  return { ...user, data: { ...user.data, iconUrl: this.defaultAvatar } };
                }
              });
            })
        }
      })
    },
    handleAgree(fid) {
      console.log('同意来自', fid, '加为好友')
      const agreedData = {
        fid: fid,
        uid: localStorage.getItem('uid'),
        result: true
      }
      handleFriendRequest(agreedData).then(res => {
        if (res.success) {
          this.$message({
            message: '已同意好友申请',
            type: 'success'
          });
          this.load()
        }
      })
    },
    handleRefuse(fid, index) {
      const refuseData = {
        fid: fid,
        uid: localStorage.getItem('uid'),
        result: false
      }
      handleFriendRequest(refuseData).then(res => {
        if (res.success) {
          this.userFriendsRequest.splice(index, 1);
          this.$message({
            message: '已拒绝好友申请',
            type: 'warning'
          });
          this.load()
        }
      })
    },
    handleImageError(event) {
      event.target.src = "https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"
    }
  },
}
</script>
<style scope>
.user-card {
  margin-top: 20px;
  /* 设置顶部外边距 */
  margin-bottom: 10px;
  /* 设置底部外边距 */
}
</style>