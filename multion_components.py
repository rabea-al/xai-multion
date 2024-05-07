from xai_components.base import InArg, OutArg, InCompArg, Component, BaseComponent, xai_component, secret
import time
import os
import requests

from multion.client import MultiOn


@xai_component
class MultiOnLogin(Component):
    api_key: InArg[secret]
    
    def execute(self, ctx):
        multion = MultiOn(api_key=self.api_key.value)
        ctx['_multion'] = multion
        ctx['_multion_api_key'] = self.api_key.value

        
@xai_component
class MultiOnNewSession(Component):
    input_prompt: InCompArg[str]
    url: InCompArg[str]
    local: InCompArg[bool]
    max_steps: InArg[int]
    
    session_id: OutArg[str]
    out_message: OutArg[str]
    status: OutArg[str]
    final_url: OutArg[str]
    screenshot_url: OutArg[str]
    step_count: OutArg[int]
    processing_time: OutArg[int]
        
    def execute(self, ctx) -> None:
        multion = ctx['_multion']

        browse = multion.browse(
            cmd=self.input_prompt.value, 
            url=self.url.value, 
            local=self.local.value,
            max_steps=self.max_steps.value if self.max_steps.value is not None else 20,
            include_screenshot=True, 
        )

        self.session_id = browse.session_id
        self.out_message.value = browse.message
        self.status.value = browse.status
        self.final_url.value = browse.url
        self.screenshot_url.value = browse.screenshot
        self.step_count = browse.metadata.step_count
        self.processing_time.value = browse.metadata.processing_time


@xai_component
class MultiOnStepSession(Component):
    input_prompt: InCompArg[str]
    session_id: InCompArg[str]
    max_steps: InArg[int]
        
    session_id: OutArg[str]
    out_message: OutArg[str]
    status: OutArg[str]
    final_url: OutArg[str]
    screenshot_url: OutArg[str]
    step_count: OutArg[int]
    processing_time: OutArg[int]
        
    def execute(self, ctx) -> None:
        multion = ctx['_multion']
        
        browse = multion.browse(
            cmd=self.input_prompt.value, 
            url=self.url.value, 
            local=self.local.value,
            session_id=self.session_id.value,
            max_steps=self.max_steps.value if self.max_steps.value is not None else 20,
            include_screenshot=True, 
        )
        
        self.out_url.value = response['url']
        self.screenshot.value = response['screenshot']
        self.message.value = response['message']
        self.status.value = response['status']


#Additional Components for Non-local APIs
#
#@xai_component
#class MultiOnListSessions(Component):
#    sessions: OutArg[list]
#
#    def execute(self, ctx) -> None:
#        api_key = ctx['_multion_api_key']
#
#        url = f"https://api.multion.ai/v1/web/sessions"
#        headers = {"X_MULTION_API_KEY": api_key}
#
#        response = requests.get(url, headers=headers)
#        res = response.json()
#        self.sessions.value = res['session_ids']
#
#
#
#@xai_component
#class MultiOnDeleteSession(Component):
#    session_id: InArg[str]
#
#    def execute(self, ctx) -> None:
#        api_key = ctx['_multion_api_key']
#
#        url = f"https://api.multion.ai/v1/web/session/{self.session_id.value}"
#        headers = {"X_MULTION_API_KEY": api_key}
#
#        response = requests.delete(url, headers=headers)
