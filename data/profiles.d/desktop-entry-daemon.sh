# set XDG_DATA_DIRS to include desktop-entry-daemon installations
echo "Setting XDG_DATA_DIRS for desktop-entry-daemon!"
new_dirs=$(
    (
        unset G_MESSAGES_DEBUG
        echo "${XDG_DATA_HOME:-"$HOME/.local/share"}/desktop-entry-daemon"
    ) | (
        new_dirs=
        while read -r install_path
        do
            share_path=$install_path/share
            case ":$XDG_DATA_DIRS:" in
                (*":$share_path:"*) :;;
                (*":$share_path/:"*) :;;
                (*) new_dirs=${new_dirs:+${new_dirs}:}$share_path;;
            esac
        done
        echo "$new_dirs"
    )
)

export XDG_DATA_DIRS
XDG_DATA_DIRS="${new_dirs:+${new_dirs}:}${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"