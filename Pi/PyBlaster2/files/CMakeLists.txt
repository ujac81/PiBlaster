
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/etc/default/pyblaster2
        DESTINATION "/etc/default"
        PERMISSIONS
          OWNER_READ OWNER_WRITE
          GROUP_READ
          WORLD_READ)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/etc/init.d/pyblaster2
        DESTINATION "/etc/init.d"
        PERMISSIONS
          OWNER_READ OWNER_WRITE OWNER_EXECUTE
          GROUP_READ GROUP_EXECUTE
          WORLD_READ WORLD_EXECUTE)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/etc/pyblaster2/pyblaster.conf
        DESTINATION "/etc/pyblaster2"
        PERMISSIONS
          OWNER_READ OWNER_WRITE
          GROUP_READ
          WORLD_READ)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/etc/profile.d/zz_pyblaster2_tmux.sh
        DESTINATION "/etc/profile.d"
        PERMISSIONS
          OWNER_READ OWNER_WRITE
          GROUP_READ
          WORLD_READ)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/opt/PyBlaster2/bin/pyblaster2-tmux.sh
        DESTINATION "/opt/PyBlaster2/bin"
        PERMISSIONS
          OWNER_READ OWNER_WRITE OWNER_EXECUTE
          GROUP_READ GROUP_EXECUTE
          WORLD_READ WORLD_EXECUTE)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/opt/PyBlaster2/bin/run-pyblaster2-terminal.sh
        DESTINATION "/opt/PyBlaster2/bin"
        PERMISSIONS
          OWNER_READ OWNER_WRITE OWNER_EXECUTE
          GROUP_READ GROUP_EXECUTE
          WORLD_READ WORLD_EXECUTE)

