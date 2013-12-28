
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/etc/default/pyblaster
        DESTINATION "/etc/default"
        PERMISSIONS
          OWNER_READ OWNER_WRITE
          GROUP_READ
          WORLD_READ)



install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/etc/init.d/pyblaster
        DESTINATION "/etc/init.d"
        PERMISSIONS
          OWNER_READ OWNER_WRITE OWNER_EXECUTE
          GROUP_READ GROUP_EXECUTE
          WORLD_READ WORLD_EXECUTE)


install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/etc/pyblaster/pyblaster.conf
        DESTINATION "/etc/pyblaster"
        PERMISSIONS
          OWNER_READ OWNER_WRITE
          GROUP_READ
          WORLD_READ)




