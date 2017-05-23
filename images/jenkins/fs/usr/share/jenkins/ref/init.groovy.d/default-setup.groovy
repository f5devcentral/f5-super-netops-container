import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount("admin","default")
hudsonRealm.createAccount("snops", "default")
instance.setSecurityRealm(hudsonRealm)

def strategy = new GlobalMatrixAuthorizationStrategy()
strategy.add(Jenkins.ADMINISTER, "admin")
strategy.add(Jenkins.ADMINISTER, "snops")
instance.setAuthorizationStrategy(strategy)
instance.save()

import jenkins.security.s2m.AdminWhitelistRule
import jenkins.model.Jenkins
Jenkins.instance.getInjector().getInstance(AdminWhitelistRule.class)
.setMasterKillSwitch(false)
