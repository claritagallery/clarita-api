;;; For more information see (info "(emacs) Directory Variables")

((nil . ((projectile-project-package-cmd . "docker build -t clarita-api:latest .")
         (projectile-project-run-cmd . "rye run dev")
         (projectile-project-test-cmd . "rye test")))
 (python-ts-mode . ((eglot-workspace-configuration . (:pylsp
                                                      (:plugins
                                                       ;; Automatically find and add missing imports
                                                       ;; https://github.com/python-lsp/python-lsp-server/blob/develop/docs/autoimport.md
                                                       ;; https://gist.github.com/doolio/8c1768ebf33c483e6d26e5205896217f
                                                       (:rope_autoimport
                                                        (:code_actions (:enabled t)
                                                         :completions (:enabled t)
                                                         :enabled t
                                                         ;; enabling in-memory DB causes python-lsp-server to hang and become unresponsive for some reason
                                                         ;; :memory t
                                                         ))
                                                       :rope_completion
                                                       (:eager :json-false
                                                               :enabled t)
                                                       )))))
 )
