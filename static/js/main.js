document.addEventListener('DOMContentLoaded', function() {
    
    // 1. 删除确认逻辑
    // 监听所有带有 'delete-confirm' 类的元素
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const confirmed = confirm("⚠️ 警告：确定要删除这条记录吗？此操作无法恢复！");
            if (!confirmed) {
                e.preventDefault(); // 取消默认跳转
            }
        });
    });

    // 2. 自动关闭 Flash 消息提示
    // 如果存在 alert 提示框，3秒后自动淡出
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alertEl => {
                // 使用 Bootstrap 的关闭实例 (如果有) 或者简单隐藏
                alertEl.style.transition = "opacity 0.5s ease";
                alertEl.style.opacity = 0;
                setTimeout(() => alertEl.remove(), 500);
            });
        }, 3000);
    }
});