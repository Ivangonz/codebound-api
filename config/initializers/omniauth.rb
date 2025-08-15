unless Rails.env.test?
  Rails.application.config.middleware.use OmniAuth::Builder do
    provider :github,
      ENV.fetch("GITHUB_CLIENT_ID"),
      ENV.fetch("GITHUB_CLIENT_SECRET"),
      scope: "read:user,user:email"
  end
end

OmniAuth.config.allowed_request_methods = %i[get post]
OmniAuth.config.silence_get_warning = true
