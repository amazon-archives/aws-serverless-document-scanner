import Vue from 'vue'
import App from './App.vue'
import VModal from 'vue-js-modal'
import Amplify, * as AmplifyModules from 'aws-amplify'
import { Auth } from 'aws-amplify'
import { AmplifyPlugin } from 'aws-amplify-vue'
import awsconfig from './aws-exports'
import apiConfig from './api-config'

Amplify.configure({
    // OPTIONAL - if your API requires authentication
    Auth: {
        // REQUIRED - Amazon Cognito Identity Pool ID
        identityPoolId: awsconfig.aws_cognito_identity_pool_id,
        // REQUIRED - Amazon Cognito Region
        region: awsconfig.aws_project_region,
        // OPTIONAL - Amazon Cognito User Pool ID
        userPoolId: awsconfig.aws_user_pools_id,
        // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
        userPoolWebClientId: awsconfig.aws_user_pools_web_client_id,
    },
    Storage: {  
      AWSS3: {
          bucket: awsconfig.aws_user_files_s3_bucket, //REQUIRED -  Amazon S3 bucket name
          region: awsconfig.aws_user_files_s3_bucket_region, //OPTIONAL -  Amazon service region
      }
    },
    API: {
        endpoints: [
            {
                name: "DocumentScannerAPI",
                endpoint: apiConfig.endpoint,
                custom_header: async () => {
                return {
                  Authorization: `Bearer ${(await Auth.currentSession()).getIdToken().getJwtToken()}`
                }
              }
            }
        ]
    }
})

Vue.use(AmplifyPlugin, AmplifyModules)
Vue.use(VModal, { dialog: true })

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')