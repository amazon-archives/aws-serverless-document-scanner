// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

// Permission is hereby granted, free of charge, to any person obtaining a copy of
// this software and associated documentation files (the "Software"), to deal in
// the Software without restriction, including without limitation the rights to
// use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
// the Software, and to permit persons to whom the Software is furnished to do so.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
// FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
// COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
// IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
// CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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
          bucket: apiConfig.s3_bucket_name, //REQUIRED -  Amazon S3 bucket name
          region: apiConfig.s3_region //OPTIONAL -  Amazon service region
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